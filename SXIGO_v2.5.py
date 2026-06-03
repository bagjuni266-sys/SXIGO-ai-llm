#!/usr/bin/env python3
"""
SXIGO AI Server v2.5 - Stability Fix
High-Performance AI Chat with GTX1660 SUPER + 4GB RAM Optimization
License: MIT
"""

import asyncio
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
import hashlib
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

try:
    import httpx
    import uvicorn
    from fastapi import FastAPI, HTTPException, Query, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.gzip import GZipMiddleware
    from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
    from pydantic import BaseModel, Field
except ImportError as e:
    print(f"❌ Missing: {e}\nRun: pip install httpx uvicorn fastapi pydantic")
    sys.exit(1)

try:
    from html.parser import HTMLParser
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self.skip = False
        def handle_starttag(self, tag, attrs):
            if tag in ('script','style','noscript','svg','iframe'):
                self.skip = True
        def handle_endtag(self, tag):
            if tag in ('script','style','noscript','svg','iframe'):
                self.skip = False
        def handle_data(self, data):
            if not self.skip:
                text = data.strip()
                if text:
                    self.text.append(text)
        def get_text(self):
            return ' '.join(self.text)
except ImportError:
    TextExtractor = None

# ==============================================================================
# LOGGING
# ==============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SXIGO_V2.5")

# ==============================================================================
# CONFIG
# ==============================================================================
CONFIG = {
    "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "server_host": os.getenv("SXIGO_HOST", "0.0.0.0"),
    "server_port": int(os.getenv("SXIGO_PORT", "8765")),
    "db_path": os.getenv("SXIGO_DB", ""),
    "default_model": os.getenv("SXIGO_MODEL", "qwen2.5-coder:7b"),
    "default_temperature": float(os.getenv("SXIGO_TEMP", "0.6")),
    "default_top_p": float(os.getenv("SXIGO_TOP_P", "0.95")),
    "default_max_tokens": int(os.getenv("SXIGO_MAX_TOKENS", "4096")),
}

DB_DIR = Path(CONFIG["db_path"]) if CONFIG["db_path"] else Path.home() / ".sxigo_v25"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "sxigo_v25.db"

# ==============================================================================
# MODELS
# ==============================================================================
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

class GenerateRequest(BaseModel):
    prompt: str
    model: str = CONFIG["default_model"]
    system: Optional[str] = None
    stream: bool = True
    temperature: float = CONFIG["default_temperature"]
    max_tokens: int = CONFIG["default_max_tokens"]

class SettingsUpdate(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None

class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 10

class WebCrawlRequest(BaseModel):
    url: str
    max_chars: int = 12000

class KnowledgeGitHubRequest(BaseModel):
    url: str
    branch: str = "main"
    max_files: int = 100
    max_chars_per_file: int = 8000

class KnowledgeQueryRequest(BaseModel):
    query: str
    max_results: int = 10
    source_id: Optional[int] = None

# ==============================================================================
# PROMPTS
# ==============================================================================
SYSTEM_PROMPTS = {
    "default": "You are SXIGO AI v2.5. Respond in user's language. Be concise yet thorough.",
    "coding": "You are SXIGO AI Coding Expert. Write clean, efficient code.",
    "creative": "You are SXIGO AI Creative. Help with writing and brainstorming.",
    "academic": "You are SXIGO AI Academic. Help with research and learning.",
    "korean": "당신은 SXIGO AI v2.5입니다. 한국어로 응답하세요.",
}

START_TIME = time.time()
_http_client: Optional[httpx.AsyncClient] = None

# ==============================================================================
# DATABASE
# ==============================================================================
def get_db():
    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-262144")
        return conn
    except Exception as e:
        logger.error(f"DB error: {e}")
        raise

def init_db():
    try:
        conn = get_db()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT DEFAULT 'Chat',
                model TEXT DEFAULT 'qwen2.5-coder:7b',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                message_count INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT CHECK(role IN ('user','assistant')),
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS knowledge_sources (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                url TEXT,
                file_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS knowledge_docs (
                id INTEGER PRIMARY KEY,
                source_id INTEGER,
                file_path TEXT,
                content TEXT,
                FOREIGN KEY(source_id) REFERENCES knowledge_sources(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations(updated_at DESC);
        """)
        conn.commit()
        conn.close()
        logger.info(f"✓ DB: {DB_PATH}")
    except Exception as e:
        logger.error(f"DB init error: {e}")
        raise

# ==============================================================================
# HTTP CLIENT
# ==============================================================================
def get_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        limits = httpx.Limits(max_keepalive_connections=50, max_connections=100, keepalive_expiry=60)
        _http_client = httpx.AsyncClient(timeout=None, limits=limits)
    return _http_client

# ==============================================================================
# FASTAPI APP
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        global _http_client
        _http_client = get_client()
        logger.info("\n" + "="*70)
        logger.info("🚀 SXIGO AI v2.5 Server")
        logger.info("="*70)
        logger.info(f"Python: {platform.python_version()}")
        logger.info(f"Ollama: {CONFIG['ollama_host']}")
        logger.info("="*70 + "\n")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    yield
    if _http_client:
        try:
            await _http_client.aclose()
            _http_client = None
        except Exception as e:
            logger.error(f"Shutdown error: {e}")

app = FastAPI(title="SXIGO AI v2.5", version="2.5.0", lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=6)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ==============================================================================
# OLLAMA
# ==============================================================================
async def ollama_request(method: str, endpoint: str, json_data: dict = None, retries: int = 1) -> dict:
    url = f"{CONFIG['ollama_host']}/api/{endpoint}"
    client = get_client()
    
    for attempt in range(retries + 1):
        try:
            if method == "GET":
                resp = await client.get(url, timeout=30)
            elif method == "POST":
                resp = await client.post(url, json=json_data or {}, timeout=60)
            elif method == "DELETE":
                resp = await client.delete(url, timeout=30)
            else:
                raise ValueError(f"Unknown method: {method}")
            resp.raise_for_status()
            return resp.json()
        except (httpx.TimeoutException, httpx.RequestError) as e:
            if attempt < retries:
                await asyncio.sleep(0.5 * (attempt + 1))
            else:
                raise HTTPException(status_code=503, detail=f"Ollama: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def ollama_stream_chat(model: str, messages: list, temperature: float, top_p: float, max_tokens: int) -> AsyncGenerator[str, None]:
    url = f"{CONFIG['ollama_host']}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {"temperature": temperature, "top_p": top_p, "num_predict": max_tokens}
    }
    client = get_client()
    try:
        async with client.stream("POST", url, json=payload, timeout=None) as response:
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
    except Exception as e:
        logger.error(f"Stream error: {e}")
        yield f"\n[Error: {str(e)}]"

async def ollama_stream_generate(prompt: str, model: str, system: str, temperature: float, max_tokens: int) -> AsyncGenerator[str, None]:
    url = f"{CONFIG['ollama_host']}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": True, "options": {"temperature": temperature, "num_predict": max_tokens}}
    if system:
        payload["system"] = system
    client = get_client()
    try:
        async with client.stream("POST", url, json=payload, timeout=None) as response:
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
    except Exception as e:
        logger.error(f"Generate error: {e}")
        yield f"\n[Error: {str(e)}]"

# ==============================================================================
# ROUTES
# ==============================================================================
HTML_PATH = Path(__file__).parent / "SXIGOai_v2.5.html"

@app.get("/")
async def root():
    if HTML_PATH.exists():
        return FileResponse(str(HTML_PATH))
    return {"name": "SXIGO AI v2.5", "status": "running", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    ollama_ok = False
    try:
        result = await ollama_request("GET", "tags")
        ollama_ok = True
    except Exception:
        pass
    return {"status": "healthy", "ollama_connected": ollama_ok, "uptime": int(time.time() - START_TIME)}

@app.get("/api/system")
async def system_info():
    return {
        "platform": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "sxigo_version": "2.5.0",
        "uptime": int(time.time() - START_TIME),
    }

@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    if not request.conversation_id:
        try:
            conn = get_db()
            title = messages_dict[-1]["content"][:50]
            conn.execute("INSERT INTO conversations (id, title, model) VALUES (?, ?, ?)", (conv_id, title, request.model))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Conv error: {e}")

    if request.stream:
        return StreamingResponse(
            stream_chat_response(conv_id, request.model, messages_dict, request.temperature, request.top_p, request.max_tokens),
            media_type="text/event-stream",
            headers={"X-Conversation-Id": conv_id}
        )
    else:
        full_response = ""
        async for chunk in ollama_stream_chat(request.model, messages_dict, request.temperature, request.top_p, request.max_tokens):
            full_response += chunk
        return {"conversation_id": conv_id, "message": {"role": "assistant", "content": full_response}}

async def stream_chat_response(conv_id: str, model: str, messages: list, temperature: float, top_p: float, max_tokens: int):
    full_response = ""
    try:
        async for chunk in ollama_stream_chat(model, messages, temperature, top_p, max_tokens):
            full_response += chunk
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'done', 'conversation_id': conv_id})}\n\n"
    except Exception as e:
        logger.error(f"Chat stream error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

@app.get("/api/conversations")
async def list_conversations(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    try:
        conn = get_db()
        rows = conn.execute("SELECT id, title, model, created_at, updated_at FROM conversations ORDER BY updated_at DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
        conn.close()
        return {"conversations": [dict(r) for r in rows], "total": total}
    except Exception as e:
        logger.error(f"List conv error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    try:
        conn = get_db()
        conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
        if not conv:
            conn.close()
            raise HTTPException(status_code=404, detail="Not found")
        messages = conn.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conv_id,)).fetchall()
        conn.close()
        return {"conversation": dict(conv), "messages": [dict(m) for m in messages]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get conv error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    try:
        conn = get_db()
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()
        conn.close()
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Delete conv error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
            models.append({"name": m["name"], "size": size_str})
        return {"models": models, "default": CONFIG["default_model"]}
    except Exception as e:
        logger.error(f"Models error: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.post("/api/generate")
async def generate_completion(request: GenerateRequest):
    try:
        if request.stream:
            return StreamingResponse(stream_generate_response(request.prompt, request.model, request.system, request.temperature, request.max_tokens), media_type="text/event-stream")
        full_response = ""
        async for chunk in ollama_stream_generate(request.prompt, request.model, request.system, request.temperature, request.max_tokens):
            full_response += chunk
        return {"response": full_response}
    except Exception as e:
        logger.error(f"Generate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_generate_response(prompt: str, model: str, system: str, temperature: float, max_tokens: int):
    try:
        async for chunk in ollama_stream_generate(prompt, model, system, temperature, max_tokens):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    except Exception as e:
        logger.error(f"Generate stream error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.get("/api/settings")
async def get_settings():
    try:
        conn = get_db()
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        conn.close()
        settings = {row["key"]: row["value"] for row in rows}
        return {
            "model": settings.get("model", CONFIG["default_model"]),
            "temperature": float(settings.get("temperature", CONFIG["default_temperature"])),
            "top_p": float(settings.get("top_p", CONFIG["default_top_p"])),
            "max_tokens": int(settings.get("max_tokens", CONFIG["default_max_tokens"])),
            "system_prompts": SYSTEM_PROMPTS
        }
    except Exception as e:
        logger.error(f"Settings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings")
async def update_settings(update: SettingsUpdate):
    try:
        conn = get_db()
        if update.model:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('model', ?)", (update.model,))
        if update.temperature is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('temperature', ?)", (str(update.temperature),))
        if update.top_p is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('top_p', ?)", (str(update.top_p),))
        if update.max_tokens is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('max_tokens', ?)", (str(update.max_tokens),))
        conn.commit()
        conn.close()
        return {"status": "saved"}
    except Exception as e:
        logger.error(f"Update settings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear")
async def clear_all():
    try:
        conn = get_db()
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
        return {"status": "cleared"}
    except Exception as e:
        logger.error(f"Clear error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/version")
async def version():
    return {"version": "2.5.0", "build": "SXIGO AI v2.5", "python": platform.python_version()}

@app.get("/api/stats")
async def get_stats():
    try:
        conn = get_db()
        stats = {
            "total_conversations": conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0],
            "total_messages": conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
        }
        conn.close()
        return stats
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# STARTUP
# ==============================================================================
def find_available_port():
    port = CONFIG["server_port"]
    for _ in range(10):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((CONFIG["server_host"], port))
            sock.close()
            return port
        except OSError:
            port += 1
    return port

def main():
    try:
        port = find_available_port()
        print("\n" + "="*80)
        print("                    🚀 SXIGO AI v2.5.0 Server                           ")
        print("="*80)
        print(f"  Ollama Host       : {CONFIG['ollama_host']}")
        print(f"  Database          : {DB_PATH}")
        print(f"  Model             : {CONFIG['default_model']}")
        print(f"  Port              : {CONFIG['server_host']}:{port}")
        print("="*80)
        print(f"\n  🌐 Open browser: http://localhost:{port}\n")
        print("="*80 + "\n")
        
        uvicorn.run(app, host=CONFIG["server_host"], port=port, log_level="info")
    except Exception as e:
        logger.error(f"Fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
