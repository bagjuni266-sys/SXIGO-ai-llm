import asyncio
import functools
import importlib.util
import json
import logging
import os
import platform
import re
import socket
import sqlite3
import sys
import time
import uuid
import urllib.parse
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

try:
    from html.parser import HTMLParser
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self.skip = False
        def handle_starttag(self, tag, attrs):
            if tag in ('script','style','noscript','svg'):
                self.skip = True
        def handle_endtag(self, tag):
            if tag in ('script','style','noscript','svg'):
                self.skip = False
        def handle_data(self, data):
            if not self.skip:
                self.text.append(data.strip())
        def get_text(self):
            return ' '.join(t for t in self.text if t)
except ImportError:
    TextExtractor = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SXIGO")

CONFIG = {
    "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "server_host": os.getenv("SXIGO_HOST", "0.0.0.0"),
    "server_port": int(os.getenv("SXIGO_PORT", "8765")),
    "db_path": os.getenv("SXIGO_DB", ""),
    "max_history": int(os.getenv("SXIGO_MAX_HISTORY", "100")),
    "default_model": os.getenv("SXIGO_MODEL", "llama3"),
    "default_temperature": float(os.getenv("SXIGO_TEMP", "0.7")),
    "default_top_p": float(os.getenv("SXIGO_TOP_P", "0.9")),
    "default_max_tokens": int(os.getenv("SXIGO_MAX_TOKENS", "8192")),
    "default_max_tokens_limit": int(os.getenv("SXIGO_MAX_TOKENS_LIMIT", "131072")),
    "enable_auth": os.getenv("SXIGO_AUTH", "false").lower() == "true",
    "auth_token": os.getenv("SXIGO_AUTH_TOKEN", ""),
}

if CONFIG["db_path"]:
    DB_DIR = Path(CONFIG["db_path"])
else:
    DB_DIR = Path.home() / ".sxigo"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "sxigo_data.db"

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: str = CONFIG["default_model"]
    messages: List[ChatMessage]
    stream: bool = True
    temperature: float = CONFIG["default_temperature"]
    top_p: float = CONFIG["default_top_p"]
    max_tokens: int = CONFIG["default_max_tokens"]
    conversation_id: Optional[str] = None

class Conversation(BaseModel):
    id: str = ""
    title: str = "New Chat"
    model: str = CONFIG["default_model"]
    created_at: str = ""
    updated_at: str = ""
    message_count: int = 0

class ModelInfo(BaseModel):
    name: str
    size: str
    modified: str

class SystemInfo(BaseModel):
    platform: str
    python_version: str
    sxigo_version: str
    ollama_connected: bool
    ollama_host: str
    uptime: str

class GenerateRequest(BaseModel):
    prompt: str
    model: str = CONFIG["default_model"]
    system: Optional[str] = None
    stream: bool = True
    temperature: float = CONFIG["default_temperature"]
    max_tokens: int = CONFIG["default_max_tokens"]

class EmbeddingsRequest(BaseModel):
    model: str = CONFIG["default_model"]
    texts: List[str]

class PullModelRequest(BaseModel):
    name: str

class DeleteModelRequest(BaseModel):
    name: str

class SettingsUpdate(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None

class KnowledgeGitHubRequest(BaseModel):
    url: str
    branch: str = "main"
    max_files: int = 50
    max_chars_per_file: int = 5000

class KnowledgeQueryRequest(BaseModel):
    query: str
    max_results: int = 5
    source_id: Optional[int] = None

SYSTEM_PROMPTS = {
    "default": "You are SXIGO AI, a helpful, creative, and intelligent assistant created by SXIGO. Respond in the same language as the user's message. Be concise yet thorough, and always provide accurate information.",
    "coding": "You are SXIGO AI Coding Assistant. Help users write clean, efficient, well-documented code. Provide explanations alongside code examples. Support all major programming languages.",
    "creative": "You are SXIGO AI Creative Assistant. Help users with creative writing, brainstorming, storytelling, poetry, and artistic endeavors. Be imaginative and inspiring.",
    "academic": "You are SXIGO AI Academic Assistant. Help with research, analysis, explanations, and learning. Provide detailed, well-structured, and cited information.",
    "korean": "You are SXIGO AI, a helpful assistant. Always respond in Korean. Be polite and formal in your responses.",
}

START_TIME = time.time()

# === OPTIMIZATION: Shared HTTP client + cache ===
_http_client: httpx.AsyncClient = None
_response_cache: dict = {}
_CACHE_TTL = 5  # seconds for API version/model list

def get_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100, keepalive_expiry=30)
        _http_client = httpx.AsyncClient(timeout=None, limits=limits, headers={"Connection": "keep-alive"})
    return _http_client

def get_cached(key: str) -> Optional[dict]:
    entry = _response_cache.get(key)
    if entry and (time.time() - entry["ts"]) < _CACHE_TTL:
        return entry["data"]
    return None

def set_cache(key: str, data: dict):
    _response_cache[key] = {"data": data, "ts": time.time()}

def clear_cache():
    _response_cache.clear()

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL DEFAULT 'New Chat',
            model TEXT NOT NULL DEFAULT 'llama3',
            system_prompt TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            message_count INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('system','user','assistant')),
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS knowledge_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('github','file','manual')),
            url TEXT,
            file_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS knowledge_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (source_id) REFERENCES knowledge_sources(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_knowledge_docs_source ON knowledge_docs(source_id);
        CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations(updated_at DESC);
    """)
    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {DB_PATH}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    global _http_client
    _http_client = get_client()
    logger.info("SXIGO AI Server starting...")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Ollama: {CONFIG['ollama_host']}")
    yield
    logger.info("SXIGO AI Server shutting down...")
    if _http_client:
        await _http_client.aclose()
        _http_client = None

app = FastAPI(title="SXIGO AI Server", version="1.0.0", lifespan=lifespan)

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_auth(request: Request):
    if not CONFIG["enable_auth"]:
        return True
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != CONFIG["auth_token"]:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    return True

async def ollama_request(method: str, endpoint: str, json_data: dict = None, retries: int = 2, use_cache: bool = False) -> dict:
    cache_key = f"{method}:{endpoint}:{json.dumps(json_data) if json_data else ''}"
    if use_cache:
        cached = get_cached(cache_key)
        if cached:
            return cached
    url = f"{CONFIG['ollama_host']}/api/{endpoint}"
    last_error = None
    client = get_client()
    for attempt in range(retries + 1):
        try:
            if method == "GET":
                resp = await client.get(url)
            elif method == "POST":
                resp = await client.post(url, json=json_data or {})
            elif method == "DELETE":
                resp = await client.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            resp.raise_for_status()
            data = resp.json()
            if use_cache:
                set_cache(cache_key, data)
            return data
        except httpx.TimeoutException:
            last_error = HTTPException(status_code=504, detail=f"Ollama request timed out (attempt {attempt + 1}/{retries + 1})")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Ollama error: {e.response.text}")
        except httpx.RequestError as e:
            last_error = HTTPException(status_code=503, detail=f"Cannot connect to Ollama at {CONFIG['ollama_host']} (attempt {attempt + 1}/{retries + 1}): {str(e)}")
        if attempt < retries:
            await asyncio.sleep(0.5 * (attempt + 1))
    raise last_error

async def ollama_stream_chat(model: str, messages: list, temperature: float, top_p: float, max_tokens: int) -> AsyncGenerator[str, None]:
    url = f"{CONFIG['ollama_host']}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": max_tokens,
        }
    }
    client = get_client()
    try:
        async with client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
    except httpx.TimeoutException:
        yield "\n\n[Error: Request timed out. The model took too long to respond.]"
    except httpx.HTTPStatusError as e:
        yield f"\n\n[Error: HTTP {e.response.status_code} - {e.response.text}]"
    except httpx.RequestError as e:
        yield f"\n\n[Error: Cannot connect to Ollama - {str(e)}]"
    except Exception as e:
        yield f"\n\n[Error: {str(e)}]"

async def ollama_stream_generate(prompt: str, model: str, system: str, temperature: float, max_tokens: int) -> AsyncGenerator[str, None]:
    url = f"{CONFIG['ollama_host']}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    if system:
        payload["system"] = system
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
        except httpx.TimeoutException:
            yield "\n\n[Error: Request timed out]"
        except httpx.HTTPStatusError as e:
            yield f"\n\n[Error: {e.response.status_code}]"
        except httpx.RequestError as e:
            yield f"\n\n[Error: Cannot connect - {str(e)}]"
        except Exception as e:
            yield f"\n\n[Error: {str(e)}]"

HTML_PATH = Path(__file__).parent / "SXIGOai.html"

@app.get("/")
async def root():
    if HTML_PATH.exists():
        return FileResponse(str(HTML_PATH))
    return {
        "name": "SXIGO AI Server",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "ollama": CONFIG["ollama_host"],
    }

@app.get("/api/health")
async def health_check():
    ollama_ok = False
    ollama_models = []
    try:
        result = await ollama_request("GET", "tags", use_cache=True)
        ollama_ok = True
        ollama_models = [m["name"] for m in result.get("models", [])]
    except Exception:
        pass
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": int(time.time() - START_TIME),
            "ollama": {
                "connected": ollama_ok,
                "host": CONFIG["ollama_host"],
                "models": ollama_models,
            },
            "database": str(DB_PATH),
        },
        headers={"X-PID": str(os.getpid())},
    )

@app.get("/api/system")
async def system_info():
    ollama_ok = False
    try:
        await ollama_request("GET", "tags")
        ollama_ok = True
    except Exception:
        pass
    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = f"{uptime_seconds // 86400}d {(uptime_seconds % 86400) // 3600}h {(uptime_seconds % 3600) // 60}m"
    return SystemInfo(
        platform=f"{platform.system()} {platform.release()}",
        python_version=platform.python_version(),
        sxigo_version="1.0.0",
        ollama_connected=ollama_ok,
        ollama_host=CONFIG["ollama_host"],
        uptime=uptime_str,
    )

@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
    conv_id = request.conversation_id or str(uuid.uuid4())
    if not request.conversation_id:
        conn = get_db()
        conn.execute(
            "INSERT INTO conversations (id, title, model) VALUES (?, ?, ?)",
            (conv_id, messages_dict[-1]["content"][:50] + "..." if len(messages_dict[-1]["content"]) > 50 else messages_dict[-1]["content"], request.model),
        )
        conn.commit()
        conn.close()
    if request.stream:
        return StreamingResponse(
            stream_chat_response(conv_id, request.model, messages_dict, request.temperature, request.top_p, request.max_tokens),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "X-Conversation-Id": conv_id,
            },
        )
    else:
        full_response = ""
        async for chunk in ollama_stream_chat(request.model, messages_dict, request.temperature, request.top_p, request.max_tokens):
            full_response += chunk
        conn = get_db()
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (conv_id, messages_dict[-1]["content"]))
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (conv_id, full_response))
        conn.execute("UPDATE conversations SET message_count = message_count + 2, updated_at = datetime('now') WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()
        return {"conversation_id": conv_id, "message": {"role": "assistant", "content": full_response}}

async def stream_chat_response(conv_id: str, model: str, messages: list, temperature: float, top_p: float, max_tokens: int):
    full_response = ""
    try:
        async for chunk in ollama_stream_chat(model, messages, temperature, top_p, max_tokens):
            full_response += chunk
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
        conn = get_db()
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (conv_id, messages[-1]["content"]))
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (conv_id, full_response))
        conn.execute("UPDATE conversations SET message_count = message_count + 2, updated_at = datetime('now') WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()
        yield f"data: {json.dumps({'type': 'done', 'conversation_id': conv_id})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

@app.post("/api/generate")
async def generate_completion(request: GenerateRequest):
    if request.stream:
        return StreamingResponse(
            stream_generate_response(request.prompt, request.model, request.system, request.temperature, request.max_tokens),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )
    full_response = ""
    async for chunk in ollama_stream_generate(request.prompt, request.model, request.system, request.temperature, request.max_tokens):
        full_response += chunk
    return {"response": full_response, "model": request.model}

async def stream_generate_response(prompt: str, model: str, system: str, temperature: float, max_tokens: int):
    async for chunk in ollama_stream_generate(prompt, model, system, temperature, max_tokens):
        yield f"data: {json.dumps({'content': chunk})}\n\n"
    yield f"data: {json.dumps({'done': True})}\n\n"

@app.get("/api/conversations")
async def list_conversations(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, model, created_at, updated_at, message_count FROM conversations ORDER BY updated_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    conn.close()
    conversations = [dict(r) for r in rows]
    return {"conversations": conversations, "total": total, "limit": limit, "offset": offset}

@app.get("/api/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    conn = get_db()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = conn.execute("SELECT id, role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
    conn.close()
    return {"conversation": dict(conv), "messages": [dict(m) for m in messages]}

@app.delete("/api/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    conn = get_db()
    conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    affected = conn.total_changes
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted", "id": conv_id}

@app.put("/api/conversations/{conv_id}")
async def update_conversation(conv_id: str, data: dict):
    conn = get_db()
    existing = conn.execute("SELECT id FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    updates = []
    params = []
    if "title" in data:
        updates.append("title = ?")
        params.append(data["title"])
    if "model" in data:
        updates.append("model = ?")
        params.append(data["model"])
    if updates:
        updates.append("updated_at = datetime('now')")
        params.append(conv_id)
        conn.execute(f"UPDATE conversations SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()
    conn.close()
    return {"status": "updated", "id": conv_id}

@app.get("/api/models")
async def list_models():
    try:
        result = await ollama_request("GET", "tags")
        models = []
        for m in result.get("models", []):
            size_bytes = m.get("size", 0)
            if size_bytes > 1073741824:
                size_str = f"{size_bytes / 1073741824:.1f} GB"
            elif size_bytes > 1048576:
                size_str = f"{size_bytes / 1048576:.1f} MB"
            else:
                size_str = f"{size_bytes / 1024:.1f} KB"
            models.append(ModelInfo(
                name=m["name"],
                size=size_str,
                modified=m.get("modified_at", "unknown"),
            ))
        return {"models": models, "default": CONFIG["default_model"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Cannot fetch models: {str(e)}")

@app.post("/api/pull")
async def pull_model(request: PullModelRequest):
    async def event_stream():
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", f"{CONFIG['ollama_host']}/api/pull", json={"name": request.name}) as resp:
                    async for line in resp.aiter_lines():
                        if line.strip():
                            yield f"data: {line}\n\n"
            yield f"data: {json.dumps({'status': 'completed', 'model': request.name})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.delete("/api/models/{model_name}")
async def delete_model(model_name: str):
    result = await ollama_request("DELETE", f"delete", {"name": model_name})
    return {"status": "deleted", "model": model_name, "result": result}

@app.post("/api/embeddings")
async def create_embeddings(request: EmbeddingsRequest):
    results = []
    for text in request.texts:
        result = await ollama_request("POST", "embeddings", {"model": request.model, "prompt": text})
        results.append(result.get("embedding", []))
    return {"model": request.model, "embeddings": results, "count": len(results)}

@app.get("/api/settings")
async def get_settings():
    conn = get_db()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    settings = {row["key"]: row["value"] for row in rows}
    return {
        "model": settings.get("model", CONFIG["default_model"]),
        "temperature": float(settings.get("temperature", CONFIG["default_temperature"])),
        "top_p": float(settings.get("top_p", CONFIG["default_top_p"])),
        "max_tokens": int(settings.get("max_tokens", CONFIG["default_max_tokens"])),
        "max_tokens_limit": CONFIG["default_max_tokens_limit"],
        "system_prompt": settings.get("system_prompt", SYSTEM_PROMPTS["default"]),
        "system_prompts": SYSTEM_PROMPTS,
    }

@app.post("/api/settings")
async def update_settings(update: SettingsUpdate):
    conn = get_db()
    if update.model is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('model', ?)", (update.model,))
    if update.temperature is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('temperature', ?)", (str(update.temperature),))
    if update.top_p is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('top_p', ?)", (str(update.top_p),))
    if update.max_tokens is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('max_tokens', ?)", (str(update.max_tokens),))
    if update.system_prompt is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('system_prompt', ?)", (update.system_prompt,))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.get("/api/templates")
async def list_templates():
    conn = get_db()
    rows = conn.execute("SELECT id, name, content, category, created_at FROM templates ORDER BY name ASC").fetchall()
    conn.close()
    return {"templates": [dict(r) for r in rows]}

@app.post("/api/templates")
async def create_template(data: dict):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO templates (name, content, category) VALUES (?, ?, ?)",
            (data["name"], data["content"], data.get("category", "general")),
        )
        conn.commit()
        template_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return {"status": "created", "id": template_id}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=409, detail="Template name already exists")

@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: int):
    conn = get_db()
    conn.execute("DELETE FROM templates WHERE id = ?", (template_id,))
    conn.commit()
    affected = conn.total_changes
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"status": "deleted"}

@app.post("/api/export")
async def export_conversation(conv_id: str):
    conn = get_db()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
    conn.close()
    export = {
        "exported_at": datetime.now().isoformat(),
        "conversation": dict(conv),
        "messages": [dict(m) for m in messages],
    }
    return JSONResponse(content=export, headers={"Content-Disposition": f'attachment; filename="sxigo_{conv_id[:8]}.json"'})

@app.post("/api/import")
async def import_conversation(data: dict):
    conn = get_db()
    conv_data = data.get("conversation", {})
    conv_id = conv_data.get("id", str(uuid.uuid4()))
    conn.execute(
        "INSERT OR REPLACE INTO conversations (id, title, model, created_at, updated_at, message_count) VALUES (?, ?, ?, ?, ?, ?)",
        (conv_id, conv_data.get("title", "Imported Chat"), conv_data.get("model", "llama3"),
         conv_data.get("created_at", datetime.now().isoformat()), datetime.now().isoformat(),
         len(data.get("messages", []))),
    )
    for msg in data.get("messages", []):
        conn.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conv_id, msg["role"], msg["content"]),
        )
    conn.commit()
    conn.close()
    return {"status": "imported", "conversation_id": conv_id}

@app.post("/api/clear")
async def clear_all():
    conn = get_db()
    conn.execute("DELETE FROM messages")
    conn.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()
    return {"status": "cleared"}

@app.get("/api/stats")
async def get_stats():
    conn = get_db()
    total_convs = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    total_msgs = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    total_user = conn.execute("SELECT COUNT(*) FROM messages WHERE role='user'").fetchone()[0]
    total_assistant = conn.execute("SELECT COUNT(*) FROM messages WHERE role='assistant'").fetchone()[0]
    top_models = conn.execute(
        "SELECT model, COUNT(*) as cnt FROM conversations GROUP BY model ORDER BY cnt DESC LIMIT 5"
    ).fetchall()
    recent = conn.execute(
        "SELECT date(created_at) as day, COUNT(*) as cnt FROM messages GROUP BY day ORDER BY day DESC LIMIT 7"
    ).fetchall()
    conn.close()
    return {
        "total_conversations": total_convs,
        "total_messages": total_msgs,
        "total_user_messages": total_user,
        "total_assistant_messages": total_assistant,
        "top_models": [dict(r) for r in top_models],
        "recent_activity": [dict(r) for r in recent],
    }

@app.post("/api/chat/title")
async def generate_title(data: dict):
    conv_id = data.get("conversation_id")
    if not conv_id:
        raise HTTPException(status_code=400, detail="conversation_id required")
    conn = get_db()
    messages = conn.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC LIMIT ?",
        (conv_id, 2),
    ).fetchall()
    conn.close()
    if not messages:
        raise HTTPException(status_code=400, detail="No messages to generate title from")
    prompt = f"Generate a very short title (max 10 words) for a conversation that starts with: {messages[0]['content'][:100]}"
    title = ""
    async for chunk in ollama_stream_generate(prompt, CONFIG["default_model"], "You generate short titles. Respond ONLY with the title, nothing else.", 0.3, 50):
        title += chunk
    title = title.strip().strip('"').strip("'")[:100]
    conn = get_db()
    conn.execute("UPDATE conversations SET title = ?, updated_at = datetime('now') WHERE id = ?", (title, conv_id))
    conn.commit()
    conn.close()
    return {"title": title}

@app.get("/api/version")
async def version():
    cache_key = "api_version"
    cached = get_cached(cache_key)
    if cached:
        return cached
    data = {
        "version": "1.0.0",
        "build": "SXIGO AI",
        "ollama_version": "0.24.0+",
        "python_version": platform.python_version(),
    }
    set_cache(cache_key, data)
    return data

class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []
        self.requests[client_id] = [t for t in self.requests[client_id] if now - t < self.window_seconds]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True

    def get_remaining(self, client_id: str) -> int:
        now = time.time()
        if client_id not in self.requests:
            return self.max_requests
        active = [t for t in self.requests[client_id] if now - t < self.window_seconds]
        return max(0, self.max_requests - len(active))

class ConversationManager:
    def __init__(self):
        self.cache: Dict[str, dict] = {}
        self.cache_ttl = 300

    def get_cached(self, conv_id: str) -> Optional[dict]:
        if conv_id in self.cache:
            entry = self.cache[conv_id]
            if time.time() - entry["cached_at"] < self.cache_ttl:
                return entry["data"]
            del self.cache[conv_id]
        return None

    def set_cached(self, conv_id: str, data: dict):
        self.cache[conv_id] = {"data": data, "cached_at": time.time()}

    def invalidate(self, conv_id: str):
        self.cache.pop(conv_id, None)

    def cleanup(self):
        now = time.time()
        expired = [k for k, v in self.cache.items() if now - v["cached_at"] >= self.cache_ttl]
        for k in expired:
            del self.cache[k]

class LoggerManager:
    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or (DB_DIR / "logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_log = self.log_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self._setup_file_logging()

    def _setup_file_logging(self):
        file_handler = logging.FileHandler(str(self.session_log), encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(file_handler)

    def log_request(self, method: str, path: str, status: int, duration: float):
        logger.info(f"[{method}] {path} -> {status} ({duration:.3f}s)")

    def log_error(self, error: Exception, context: str = ""):
        logger.error(f"{context}: {type(error).__name__}: {str(error)}")

    def cleanup_old_logs(self, days: int = 7):
        cutoff = time.time() - (days * 86400)
        for log_file in self.log_dir.glob("session_*.log"):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                logger.info(f"Removed old log: {log_file.name}")

class MiddlewareManager:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware):
        self.middlewares.append(middleware)

    async def process_request(self, request: Request):
        for m in self.middlewares:
            result = await m.process_request(request)
            if result:
                return result
        return None

    async def process_response(self, request: Request, response):
        for m in reversed(self.middlewares):
            await m.process_response(request, response)

class CORSMiddlewareConfig:
    def __init__(self):
        self.allowed_origins = ["*"]
        self.allowed_methods = ["*"]
        self.allowed_headers = ["*"]

class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.request_counts: Dict[str, int] = {}
        self.model_usage: Dict[str, int] = {}
        self.start_time = time.time()

    def record_request(self, path: str, duration: float, status: int):
        self.request_count += 1
        self.total_response_time += duration
        self.request_counts[path] = self.request_counts.get(path, 0) + 1
        if status >= 400:
            self.error_count += 1

    def record_model_usage(self, model: str):
        self.model_usage[model] = self.model_usage.get(model, 0) + 1

    def get_metrics(self) -> dict:
        uptime = time.time() - self.start_time
        avg_response = self.total_response_time / max(self.request_count, 1)
        return {
            "uptime_seconds": uptime,
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate": f"{(self.error_count / max(self.request_count, 1)) * 100:.2f}%",
            "average_response_time": f"{avg_response:.3f}s",
            "requests_per_second": f"{self.request_count / max(uptime, 1):.2f}",
            "requests_by_endpoint": self.request_counts,
            "model_usage": self.model_usage,
        }

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, dict] = {}
        self.plugin_dir = DB_DIR / "plugins"
        self.plugin_dir.mkdir(parents=True, exist_ok=True)

    def discover_plugins(self):
        if not self.plugin_dir.exists():
            return
        for plugin_file in self.plugin_dir.glob("*.py"):
            try:
                plugin_name = plugin_file.stem
                if plugin_name.startswith("_"):
                    continue
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "setup"):
                        plugin_info = module.setup()
                        self.plugins[plugin_name] = {
                            "module": module,
                            "info": plugin_info,
                            "loaded_at": datetime.now().isoformat(),
                        }
                        logger.info(f"Loaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file.name}: {e}")

    def get_plugin_info(self, name: str) -> Optional[dict]:
        plugin = self.plugins.get(name)
        if plugin:
            return {"name": name, **plugin["info"], "loaded_at": plugin["loaded_at"]}
        return None

    def list_plugins(self) -> list:
        return [{"name": name, **p["info"], "loaded_at": p["loaded_at"]} for name, p in self.plugins.items()]

class ResponseFormatter:
    @staticmethod
    def format_markdown(text: str) -> str:
        lines = text.split("\n")
        formatted = []
        in_code_block = False
        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                formatted.append(line)
                continue
            if not in_code_block:
                if line.strip().startswith("#"):
                    formatted.append(line)
                elif line.strip().startswith(("- ", "* ", "+ ")):
                    formatted.append(line)
                elif line.strip() and line.strip()[0].isdigit() and ". " in line.strip()[:4]:
                    formatted.append(line)
                else:
                    formatted.append(line)
            else:
                formatted.append(line)
        return "\n".join(formatted)

    @staticmethod
    def truncate(text: str, max_length: int = 2000, suffix: str = "...") -> str:
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(" ", 1)[0] + suffix

    @staticmethod
    def extract_code_blocks(text: str) -> list:
        import re
        pattern = r"```(\w*)\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return [{"language": lang or "text", "code": code.strip()} for lang, code in matches]

class CacheManager:
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, tuple] = {}
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            del self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        if len(self.cache) >= self.max_size:
            oldest = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest]
        self.cache[key] = (value, time.time() + ttl)

    def clear(self):
        self.cache.clear()

    def remove(self, key: str):
        self.cache.pop(key, None)

class WebSocketManager:
    def __init__(self):
        self.connections: Dict[str, list] = {}

    async def connect(self, conv_id: str, websocket):
        if conv_id not in self.connections:
            self.connections[conv_id] = []
        self.connections[conv_id].append(websocket)

    async def disconnect(self, conv_id: str, websocket):
        if conv_id in self.connections:
            self.connections[conv_id] = [ws for ws in self.connections[conv_id] if ws != websocket]
            if not self.connections[conv_id]:
                del self.connections[conv_id]

    async def broadcast(self, conv_id: str, message: dict):
        if conv_id in self.connections:
            for ws in self.connections[conv_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass

class SearchEngine:
    def __init__(self):
        self.index: Dict[str, list] = {}

    def index_conversation(self, conv_id: str, messages: list):
        words = set()
        for msg in messages:
            content = msg.get("content", "")
            words.update(content.lower().split())
        self.index[conv_id] = list(words)

    def search(self, query: str, limit: int = 10) -> list:
        query_words = set(query.lower().split())
        results = []
        for conv_id, words in self.index.items():
            score = len(query_words & set(words))
            if score > 0:
                results.append({"conversation_id": conv_id, "score": score})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def remove(self, conv_id: str):
        self.index.pop(conv_id, None)

class BatchProcessor:
    def __init__(self, max_batch: int = 10):
        self.max_batch = max_batch
        self.queue: list = []

    def add(self, item: dict):
        self.queue.append(item)

    async def process_all(self) -> list:
        results = []
        while self.queue:
            batch = self.queue[:self.max_batch]
            self.queue = self.queue[self.max_batch:]
            for item in batch:
                try:
                    if item["type"] == "chat":
                        async for chunk in ollama_stream_chat(
                            item.get("model", CONFIG["default_model"]),
                            item.get("messages", []),
                            item.get("temperature", CONFIG["default_temperature"]),
                            item.get("top_p", CONFIG["default_top_p"]),
                            item.get("max_tokens", CONFIG["default_max_tokens"]),
                        ):
                            pass
                        results.append({"item": item, "status": "completed"})
                    else:
                        results.append({"item": item, "status": "skipped", "reason": "unknown type"})
                except Exception as e:
                    results.append({"item": item, "status": "error", "error": str(e)})
        return results

class PromptTemplate:
    def __init__(self, name: str, content: str, variables: list = None):
        self.name = name
        self.content = content
        self.variables = variables or []

    def render(self, **kwargs) -> str:
        result = self.content
        for var, value in kwargs.items():
            result = result.replace(f"{{{{{var}}}}}", str(value))
        return result

    def validate(self) -> bool:
        import re
        missing = re.findall(r"\{\{(\w+)\}\}", self.content)
        return len(missing) == 0

class ConfigValidator:
    @staticmethod
    def validate_port(port: int) -> bool:
        return 1024 <= port <= 65535

    @staticmethod
    def validate_temperature(temp: float) -> bool:
        return 0.0 <= temp <= 2.0

    @staticmethod
    def validate_top_p(p: float) -> bool:
        return 0.0 <= p <= 1.0

    @staticmethod
    def validate_max_tokens(tokens: int) -> bool:
        return 1 <= tokens <= 999999

    @staticmethod
    def validate_model_name(name: str) -> bool:
        return bool(name) and len(name) <= 100

    @staticmethod
    def validate_all(config: dict) -> dict:
        errors = {}
        if "server_port" in config and not ConfigValidator.validate_port(config["server_port"]):
            errors["server_port"] = "Must be between 1024 and 65535"
        if "default_temperature" in config and not ConfigValidator.validate_temperature(config["default_temperature"]):
            errors["default_temperature"] = "Must be between 0.0 and 2.0"
        if "default_top_p" in config and not ConfigValidator.validate_top_p(config["default_top_p"]):
            errors["default_top_p"] = "Must be between 0.0 and 1.0"
        if "default_max_tokens" in config and not ConfigValidator.validate_max_tokens(config["default_max_tokens"]):
            errors["default_max_tokens"] = "Must be between 1 and 131072"
        return errors

class HealthChecker:
    def __init__(self):
        self.checks: Dict[str, callable] = {}

    def register(self, name: str, check_fn: callable):
        self.checks[name] = check_fn

    async def run_all(self) -> dict:
        results = {}
        for name, check_fn in self.checks.items():
            try:
                if asyncio.iscoroutinefunction(check_fn):
                    result = await check_fn()
                else:
                    result = check_fn()
                results[name] = {"status": "ok", "detail": str(result) if result else "passed"}
            except Exception as e:
                results[name] = {"status": "error", "detail": str(e)}
        return results

rate_limiter = RateLimiter()
conv_manager = ConversationManager()
log_manager = LoggerManager()
metrics = MetricsCollector()
plugin_manager = PluginManager()
cache_manager = CacheManager()
ws_manager = WebSocketManager()
search_engine = SearchEngine()
batch_processor = BatchProcessor()
health_checker = HealthChecker()

health_checker.register("database", lambda: get_db().execute("SELECT 1").fetchone())
health_checker.register("ollama", lambda: ollama_request("GET", "tags"))
health_checker.register("disk_space", lambda: (DB_DIR.stat().st_dev, "available"))

@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        metrics.record_request(request.url.path, duration, response.status_code)
        log_manager.log_request(request.method, request.url.path, response.status_code, duration)
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        response.headers["X-SXIGO-Version"] = "1.0.0"
        if request.url.path.startswith("/api/chat"):
            response.headers["Cache-Control"] = "no-cache, no-transform"
            response.headers["X-Accel-Buffering"] = "no"
        return response
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_request(request.url.path, duration, 500)
        log_manager.log_error(e, f"Request failed: {request.method} {request.url.path}")
        raise

@app.get("/api/metrics")
async def get_metrics():
    return metrics.get_metrics()

@app.get("/api/plugins")
async def list_plugin_info():
    return {"plugins": plugin_manager.list_plugins()}

@app.post("/api/plugins/reload")
async def reload_plugins():
    plugin_manager.discover_plugins()
    return {"status": "reloaded", "count": len(plugin_manager.plugins)}

@app.get("/api/health/full")
async def full_health_check():
    results = await health_checker.run_all()
    overall = all(r["status"] == "ok" for r in results.values())
    return {
        "status": "healthy" if overall else "degraded",
        "timestamp": datetime.now().isoformat(),
        "checks": results,
    }

@app.get("/api/logs")
async def get_logs(lines: int = Query(50, ge=10, le=500)):
    log_file = log_manager.session_log
    if not log_file.exists():
        return {"logs": []}
    content = log_file.read_text(encoding="utf-8").strip().split("\n")
    return {"logs": content[-lines:], "total_lines": len(content)}

@app.get("/api/search")
async def search_conversations(q: str = Query("", min_length=1), limit: int = Query(10, ge=1, le=50)):
    results = search_engine.search(q, limit)
    conn = get_db()
    conv_ids = [r["conversation_id"] for r in results]
    conversations = []
    for cid in conv_ids:
        conv = conn.execute("SELECT id, title, model, updated_at FROM conversations WHERE id = ?", (cid,)).fetchone()
        if conv:
            conversations.append(dict(conv))
    conn.close()
    return {"query": q, "results": conversations, "count": len(conversations)}

@app.get("/api/cache/status")
async def cache_status():
    return {
        "size": len(cache_manager.cache),
        "max_size": cache_manager.max_size,
    }

@app.post("/api/cache/clear")
async def clear_cache():
    cache_manager.clear()
    return {"status": "cleared"}

@app.get("/api/chat/{conv_id}/search")
async def search_in_conversation(conv_id: str, q: str = Query("", min_length=1)):
    conn = get_db()
    messages = conn.execute(
        "SELECT id, role, content, created_at FROM messages WHERE conversation_id = ? AND content LIKE ? ORDER BY id ASC",
        (conv_id, f"%{q}%"),
    ).fetchall()
    conn.close()
    return {"query": q, "matches": [dict(m) for m in messages], "count": len(messages)}

@app.post("/api/conversations/{conv_id}/archive")
async def archive_conversation(conv_id: str):
    conn = get_db()
    conn.execute("UPDATE conversations SET title = '[Archived] ' || title WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()
    return {"status": "archived", "id": conv_id}

@app.post("/api/conversations/batch-delete")
async def batch_delete_conversations(data: dict):
    ids = data.get("ids", [])
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    conn = get_db()
    placeholders = ",".join("?" * len(ids))
    conn.execute(f"DELETE FROM conversations WHERE id IN ({placeholders})", ids)
    conn.commit()
    conn.close()
    return {"status": "deleted", "count": len(ids)}

@app.get("/api/conversations/search")
async def search_conversations_by_title(q: str = Query("", min_length=1)):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, model, created_at, updated_at, message_count FROM conversations WHERE title LIKE ? ORDER BY updated_at DESC LIMIT 50",
        (f"%{q}%",),
    ).fetchall()
    conn.close()
    return {"conversations": [dict(r) for r in rows]}

@app.post("/api/conversations/merge")
async def merge_conversations(data: dict):
    source_ids = data.get("source_ids", [])
    target_id = data.get("target_id")
    if not source_ids or not target_id:
        raise HTTPException(status_code=400, detail="source_ids and target_id required")
    conn = get_db()
    for sid in source_ids:
        if sid == target_id:
            continue
        conn.execute(
            "UPDATE messages SET conversation_id = ? WHERE conversation_id = ?",
            (target_id, sid),
        )
        conn.execute("DELETE FROM conversations WHERE id = ?", (sid,))
    conn.execute(
        "UPDATE conversations SET message_count = (SELECT COUNT(*) FROM messages WHERE conversation_id = ?), updated_at = datetime('now') WHERE id = ?",
        (target_id, target_id),
    )
    conn.commit()
    conn.close()
    return {"status": "merged", "target": target_id}

@app.post("/api/conversations/{conv_id}/duplicate")
async def duplicate_conversation(conv_id: str):
    conn = get_db()
    original = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not original:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    new_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO conversations (id, title, model, created_at, updated_at, message_count) VALUES (?, ?, ?, datetime('now'), datetime('now'), ?)",
        (new_id, original["title"] + " (Copy)", original["model"], original["message_count"]),
    )
    messages = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
    for msg in messages:
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", (new_id, msg["role"], msg["content"]))
    conn.commit()
    conn.close()
    return {"status": "duplicated", "new_id": new_id}

@app.post("/api/conversations/{conv_id}/export/markdown")
async def export_as_markdown(conv_id: str):
    conn = get_db()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
    conn.close()
    lines = [f"# {conv['title']}", f"", f"Model: {conv['model']}", f"Date: {conv['created_at']}", f"", "---", ""]
    for msg in messages:
        if msg["role"] == "user":
            lines.append(f"## User")
        else:
            lines.append(f"## Assistant")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
        lines.append("---")
        lines.append("")
    content = "\n".join(lines)
    return Response(content=content, media_type="text/markdown", headers={"Content-Disposition": f'attachment; filename="sxigo_{conv_id[:8]}.md"'})

@app.post("/api/conversations/{conv_id}/export/html")
async def export_as_html(conv_id: str):
    conn = get_db()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
    conn.close()
    html_parts = [f"<html><head><meta charset='utf-8'><title>{conv['title']}</title><style>body{{max-width:800px;margin:auto;padding:20px;font-family:sans-serif;background:#1a1a2e;color:#e0e0e0}}.user{{background:#16213e;padding:15px;border-radius:10px;margin:10px 0}}.assistant{{background:#1a1a3e;padding:15px;border-radius:10px;margin:10px 0;border-left:4px solid #e94560}}</style></head><body>"]
    html_parts.append(f"<h1>{conv['title']}</h1><p><em>Model: {conv['model']} | Date: {conv['created_at']}</em></p><hr>")
    for msg in messages:
        role_class = msg["role"]
        html_parts.append(f"<div class='{role_class}'><strong>{'User' if msg['role']=='user' else 'Assistant'}:</strong><br>{msg['content']}</div>")
    html_parts.append("</body></html>")
    content = "\n".join(html_parts)
    return Response(content=content, media_type="text/html", headers={"Content-Disposition": f'attachment; filename="sxigo_{conv_id[:8]}.html"'})

@app.post("/api/batch/chat")
async def batch_chat(data: dict):
    requests = data.get("requests", [])
    for req in requests:
        batch_processor.add(req)
    results = await batch_processor.process_all()
    return {"results": results, "count": len(results)}

@app.get("/api/database/info")
async def database_info():
    conn = get_db()
    size = os.path.getsize(str(DB_PATH)) if DB_PATH.exists() else 0
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    conn.close()
    if size > 1048576:
        size_str = f"{size / 1048576:.2f} MB"
    elif size > 1024:
        size_str = f"{size / 1024:.2f} KB"
    else:
        size_str = f"{size} B"
    return {
        "path": str(DB_PATH),
        "size": size_str,
        "size_bytes": size,
        "tables": [t["name"] for t in tables],
    }

@app.post("/api/database/vacuum")
async def vacuum_database():
    conn = get_db()
    conn.execute("VACUUM")
    conn.close()
    return {"status": "vacuumed"}

@app.post("/api/database/backup")
async def backup_database():
    backup_path = DB_DIR / f"sxigo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    conn = get_db()
    backup_conn = sqlite3.connect(str(backup_path))
    conn.backup(backup_conn)
    backup_conn.close()
    conn.close()
    return {"status": "backup_created", "path": str(backup_path)}

@app.post("/api/chat/{conv_id}/regenerate")
async def regenerate_last_response(conv_id: str):
    conn = get_db()
    messages = conn.execute(
        "SELECT id, role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conv_id,),
    ).fetchall()
    if len(messages) < 2:
        conn.close()
        raise HTTPException(status_code=400, detail="Not enough messages to regenerate")
    last_assistant = messages[-1]
    if last_assistant["role"] != "assistant":
        conn.close()
        raise HTTPException(status_code=400, detail="Last message is not from assistant")
    conn.execute("DELETE FROM messages WHERE id = ?", (last_assistant["id"],))
    conn.execute("UPDATE conversations SET message_count = message_count - 1 WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()
    chat_messages = [{"role": m["role"], "content": m["content"]} for m in messages[:-1]]
    return StreamingResponse(
        stream_chat_response(conv_id, CONFIG["default_model"], chat_messages, CONFIG["default_temperature"], CONFIG["default_top_p"], CONFIG["default_max_tokens"]),
        media_type="text/event-stream",
    )

@app.post("/api/chat/{conv_id}/edit")
async def edit_message(conv_id: str, data: dict):
    message_id = data.get("message_id")
    new_content = data.get("content")
    if not message_id or not new_content:
        raise HTTPException(status_code=400, detail="message_id and content required")
    conn = get_db()
    conn.execute("UPDATE messages SET content = ? WHERE id = ? AND conversation_id = ?", (new_content, message_id, conv_id))
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.post("/api/chat/{conv_id}/fork")
async def fork_conversation(conv_id: str, data: dict):
    message_id = data.get("message_id")
    if not message_id:
        raise HTTPException(status_code=400, detail="message_id required")
    conn = get_db()
    original = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not original:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    new_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO conversations (id, title, model, created_at, updated_at, message_count) VALUES (?, ?, ?, datetime('now'), datetime('now'), 0)",
        (new_id, original["title"] + " (Fork)", original["model"]),
    )
    messages = conn.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? AND id <= ? ORDER BY id ASC",
        (conv_id, message_id),
    ).fetchall()
    for msg in messages:
        conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)", (new_id, msg["role"], msg["content"]))
    conn.execute(
        "UPDATE conversations SET message_count = (SELECT COUNT(*) FROM messages WHERE conversation_id = ?) WHERE id = ?",
        (new_id, new_id),
    )
    conn.commit()
    conn.close()
    return {"status": "forked", "new_id": new_id}

@app.get("/api/config")
async def get_config():
    safe_config = {k: v for k, v in CONFIG.items() if k != "auth_token"}
    return {"config": safe_config, "validations": ConfigValidator.validate_all(CONFIG)}

@app.post("/api/config/reload")
async def reload_config():
    global CONFIG
    CONFIG["ollama_host"] = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    CONFIG["server_host"] = os.getenv("SXIGO_HOST", "0.0.0.0")
    CONFIG["server_port"] = int(os.getenv("SXIGO_PORT", "8765"))
    CONFIG["default_model"] = os.getenv("SXIGO_MODEL", "llama3")
    CONFIG["default_temperature"] = float(os.getenv("SXIGO_TEMP", "0.7"))
    CONFIG["default_max_tokens"] = int(os.getenv("SXIGO_MAX_TOKENS", "4096"))
    logger.info("Configuration reloaded")
    return {"status": "reloaded"}

@app.get("/api/debug/env")
async def debug_env():
    return {
        "ollama_host": CONFIG["ollama_host"],
        "server_host": CONFIG["server_host"],
        "server_port": CONFIG["server_port"],
        "db_path": str(DB_PATH),
        "db_dir": str(DB_DIR),
        "python": platform.python_version(),
        "platform": platform.system(),
        "cwd": os.getcwd(),
        "pid": os.getpid(),
    }

@app.post("/api/test/ollama")
async def test_ollama():
    results = {}
    try:
        t0 = time.time()
        tags = await ollama_request("GET", "tags")
        t1 = time.time()
        results["list_models"] = {"status": "ok", "time": f"{t1-t0:.3f}s", "count": len(tags.get("models", []))}
    except Exception as e:
        results["list_models"] = {"status": "error", "error": str(e)}
    try:
        t0 = time.time()
        async for chunk in ollama_stream_chat(CONFIG["default_model"], [{"role": "user", "content": "Say 'Hello' and nothing else."}], 0.1, 0.9, 10):
            pass
        t1 = time.time()
        results["chat_test"] = {"status": "ok", "time": f"{t1-t0:.3f}s"}
    except Exception as e:
        results["chat_test"] = {"status": "error", "error": str(e)}
    return results

class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 10

class WebCrawlRequest(BaseModel):
    url: str
    max_chars: int = 8000

CRAWL_HEADERS = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Connection": "keep-alive",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
    },
    {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
    },
]

DDG_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
}

@app.post("/api/web/search")
async def web_search(req: WebSearchRequest):
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        encoded = urllib.parse.quote(query)
        url = f"https://lite.duckduckgo.com/lite/?q={encoded}"
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=DDG_HEADERS)
            resp.raise_for_status()
            html = resp.text
        results = []
        lines = html.split("\n")
        current = {}
        for line in lines:
            line = line.strip()
            if 'class="result-link"' in line or 'class="result-snippet"' in line:
                pass
            if 'class="result-title' in line or 'class="result__title' in line or 'class="result-link' in line:
                href_match = re.search(r'href="([^"]+)"', line)
                text_match = re.search(r'>([^<]+)<', line)
                if href_match and text_match:
                    current["url"] = href_match.group(1)
                    current["title"] = text_match.group(1).strip()
                    if "url" in current and "title" in current:
                        results.append(current)
                        current = {}
                        if len(results) >= req.max_results:
                            break
            if 'class="result-snippet"' in line or 'class="result__snippet"' in line:
                txt = re.sub(r'<[^>]+>', '', line).strip()
                if txt:
                    current["snippet"] = txt
        if not results:
            soup_re = re.compile(r'<a[^>]+rel="nofollow"[^>]*>([^<]+)</a>', re.IGNORECASE)
            for m in soup_re.finditer(html):
                title = m.group(1).strip()
                if title:
                    soup_link = re.compile(r'<a[^>]+href="([^"]+)"[^>]*>')
                    for lm in soup_link.finditer(html):
                        results.append({"title": title, "url": lm.group(1), "snippet": ""})
                        if len(results) >= req.max_results:
                            break
                if len(results) >= req.max_results:
                    break
        return {"query": req.query, "results": results[:req.max_results], "count": len(results[:req.max_results])}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Search request timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Search service error: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/web/crawl")
async def web_crawl(req: WebCrawlRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    last_error = None
    for attempt in range(2):
        for headers in CRAWL_HEADERS:
            try:
                async with httpx.AsyncClient(timeout=15.0, follow_redirects=True, verify=False) as client:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code >= 400:
                        last_error = f"HTTP {resp.status_code}"
                        continue
                    content_type = resp.headers.get("content-type", "")
                    raw = resp.text
                    title = ""
                    title_match = re.search(r'<title[^>]*>([^<]+)</title>', raw, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1).strip()
                    text_content = raw
                    if "text/html" in content_type:
                        try:
                            if TextExtractor is not None:
                                extractor = TextExtractor()
                                extractor.feed(raw)
                                text_content = extractor.get_text()
                            else:
                                text_content = re.sub(r'<[^>]+>', ' ', raw)
                                text_content = re.sub(r'\s+', ' ', text_content).strip()
                        except Exception:
                            text_content = re.sub(r'<[^>]+>', ' ', raw)
                            text_content = re.sub(r'\s+', ' ', text_content).strip()
                    else:
                        text_content = raw[:req.max_chars]
                    text_content = re.sub(r'\s+', ' ', text_content).strip()
                    if len(text_content) > req.max_chars:
                        text_content = text_content[:req.max_chars] + "..."
                    return {
                        "url": url,
                        "title": title,
                        "content": text_content,
                        "content_type": content_type,
                        "content_length": len(raw),
                        "truncated": len(raw) > req.max_chars,
                    }
            except httpx.TimeoutException:
                last_error = "timeout"
                continue
            except (httpx.ConnectError, httpx.ConnectTimeout):
                last_error = "connection_failed"
                continue
            except httpx.RemoteProtocolError:
                last_error = "protocol_error"
                continue
            except Exception as e:
                last_error = str(e)
                continue

    if last_error == "timeout":
        raise HTTPException(status_code=504, detail="Crawl request timed out after retries")
    elif last_error == "connection_failed":
        raise HTTPException(status_code=502, detail="Cannot connect to the website — the site may be blocking automated requests or does not exist")
    elif last_error and last_error.startswith("HTTP "):
        raise HTTPException(status_code=502, detail=f"Website returned {last_error} — the page may require login or does not exist")
    else:
        raise HTTPException(status_code=502, detail=f"Failed to crawl page: {last_error or 'unknown error'}")

@app.get("/api/web/search")
async def web_search_get(q: str = Query("", min_length=1), max_results: int = Query(10, ge=1, le=20)):
    return await web_search(WebSearchRequest(query=q, max_results=max_results))

@app.get("/api/web/crawl")
async def web_crawl_get(url: str = Query(""), max_chars: int = Query(8000, ge=500, le=50000)):
    return await web_crawl(WebCrawlRequest(url=url, max_chars=max_chars))

# ============================================================
#  KNOWLEDGE BASE API
# ============================================================
GITHUB_API_HEADERS = {
    "User-Agent": "SXIGO-AI/1.0",
    "Accept": "application/vnd.github.v3+json",
}

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".scss", ".less",
    ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".md", ".rst", ".txt", ".csv", ".tsv",
    ".c", ".cpp", ".h", ".hpp", ".java", ".kt", ".swift", ".go", ".rs",
    ".rb", ".php", ".pl", ".pm", ".sh", ".bash", ".zsh", ".ps1",
    ".sql", ".r", ".m", ".mm",
    ".vue", ".svelte", ".astro",
    ".gradle", ".properties", ".env", ".gitignore", ".dockerfile",
    ".proto", ".graphql", ".gql",
}

def is_text_file(path: str) -> bool:
    ext = Path(path).suffix.lower()
    name = Path(path).name.lower()
    return ext in TEXT_EXTENSIONS or name in ("dockerfile", "makefile", "gemfile", "requirements.txt", "pipfile")

@app.post("/api/knowledge/github")
async def knowledge_github(req: KnowledgeGitHubRequest):
    url = req.url.strip().rstrip("/")
    if url.startswith("github.com/"):
        url = "https://" + url
    # Parse owner/repo from URL
    m = re.search(r"github\.com[:/]([^/]+)/([^/?#]+)", url)
    if not m:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")
    owner, repo = m.group(1), m.group(2)
    repo = re.sub(r'\.git$', '', repo)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{req.branch}?recursive=1"
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(api_url, headers=GITHUB_API_HEADERS)
            if resp.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Repository {owner}/{repo} not found")
            if resp.status_code == 403:
                raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded. Try again later.")
            resp.raise_for_status()
            tree_data = resp.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="GitHub API request timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {str(e)}")

    files = [item for item in tree_data.get("tree", []) if item["type"] == "blob" and is_text_file(item["path"])]
    files = files[:req.max_files]
    if not files:
        raise HTTPException(status_code=404, detail="No text/code files found in this repository")

    source_name = f"{owner}/{repo}"
    conn = get_db()
    cur = conn.execute("INSERT INTO knowledge_sources (name, type, url) VALUES (?, 'github', ?)", (source_name, url))
    source_id = cur.lastrowid

    downloaded = 0
    failed = 0
    for item in files:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{req.branch}/{item['path']}"
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                r = await client.get(raw_url)
                if r.status_code == 200:
                    content = r.text[:req.max_chars_per_file]
                    conn.execute(
                        "INSERT INTO knowledge_docs (source_id, file_path, content) VALUES (?, ?, ?)",
                        (source_id, item["path"], content)
                    )
                    downloaded += 1
                else:
                    failed += 1
        except Exception:
            failed += 1

    conn.execute("UPDATE knowledge_sources SET file_count = ? WHERE id = ?", (downloaded, source_id))
    conn.commit()
    conn.close()
    return {
        "source_id": source_id,
        "name": source_name,
        "files_found": len(files),
        "downloaded": downloaded,
        "failed": failed,
    }

@app.get("/api/knowledge")
async def knowledge_list():
    conn = get_db()
    rows = conn.execute("SELECT id, name, type, url, file_count, created_at FROM knowledge_sources ORDER BY created_at DESC").fetchall()
    conn.close()
    return {"sources": [dict(r) for r in rows]}

@app.delete("/api/knowledge/{source_id}")
async def knowledge_delete(source_id: int):
    conn = get_db()
    cur = conn.execute("DELETE FROM knowledge_sources WHERE id = ?", (source_id,))
    conn.execute("DELETE FROM knowledge_docs WHERE source_id = ?", (source_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Knowledge source not found")
    return {"status": "deleted"}

@app.post("/api/knowledge/query")
async def knowledge_query(req: KnowledgeQueryRequest):
    query = req.query.strip().lower()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    keywords = [w for w in re.split(r'[^\w가-힣]+', query) if len(w) > 1]
    if not keywords:
        return {"query": query, "results": []}
    conn = get_db()
    sql = "SELECT id, source_id, file_path, content FROM knowledge_docs"
    params = []
    if req.source_id:
        sql += " WHERE source_id = ?"
        params.append(req.source_id)
    rows = conn.execute(sql, params).fetchall()
    scored = []
    for row in rows:
        content_lower = row["content"].lower()
        path_lower = row["file_path"].lower()
        score = 0
        for kw in keywords:
            if kw in content_lower:
                score += content_lower.count(kw) * 2
            if kw in path_lower:
                score += 5
        if score > 0:
            scored.append((score, row["id"], row["source_id"], row["file_path"], row["content"]))
    scored.sort(key=lambda x: -x[0])
    conn.close()
    results = []
    for score, doc_id, src_id, file_path, content in scored[:req.max_results]:
        ctx = content[:1000] + "..." if len(content) > 1000 else content
        results.append({"id": doc_id, "source_id": src_id, "file_path": file_path, "content": ctx, "score": score})
    return {"query": req.query, "results": results, "total_matches": len(scored)}

def find_available_port():
    port = CONFIG["server_port"]
    for _ in range(10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((CONFIG["server_host"], port))
            sock.close()
            return port
        except OSError:
            sock.close()
            print(f"  Port {port} is in use, trying {port + 1}...")
            port += 1
    print(f"  Could not find available port, using {port} anyway")
    return port

def main():
    port = find_available_port()
    print()
    print("=" * 60)
    print("           SXIGO AI Server v1.0.0")
    print("=" * 60)
    print(f"  Ollama  : {CONFIG['ollama_host']}")
    print(f"  HTML    : {HTML_PATH}")
    print(f"  DB      : {DB_PATH}")
    print(f"  Model   : {CONFIG['default_model']}")
    print(f"  Auth    : {'Enabled' if CONFIG['enable_auth'] else 'Disabled'}")
    print(f"  Logs    : {log_manager.session_log}")
    print(f"  Listen  : {CONFIG['server_host']}:{port}")
    print(f"  Web     : http://localhost:{port}")
    print(f"  Web     : http://127.0.0.1:{port}")
    print("=" * 60)
    print()
    print(f"  >>> Open your browser and go to: http://localhost:{port} <<<")
    print()
    uvicorn.run(app, host=CONFIG["server_host"], port=port, log_level="info", http="httptools", server_header=True)

if __name__ == "__main__":
    main()
