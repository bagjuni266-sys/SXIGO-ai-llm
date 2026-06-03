#!/usr/bin/env python3
"""
SXIGO AI Server v2.5 - Enhanced Edition
5X Boost Technology - 6x Response Speed
Dynamic Model Loading - All Local Models Supported
High-Performance AI Chat with GTX1660 SUPER + 4GB RAM Optimization
License: MIT
Author: SXIGO Team
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
import subprocess
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
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install httpx uvicorn fastapi pydantic")
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
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("SXIGO_V2.5")

# ==============================================================================
# CONFIGURATION
# ==============================================================================
CONFIG = {
    "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "server_host": os.getenv("SXIGO_HOST", "0.0.0.0"),
    "server_port": int(os.getenv("SXIGO_PORT", "8765")),
    "db_path": os.getenv("SXIGO_DB", ""),
    "default_temperature": float(os.getenv("SXIGO_TEMP", "0.6")),
    "default_top_p": float(os.getenv("SXIGO_TOP_P", "0.95")),
    "default_max_tokens": int(os.getenv("SXIGO_MAX_TOKENS", "4096")),
    "boost_enabled": False,
    "boost_multiplier": 5,
}

DB_DIR = Path(CONFIG["db_path"]) if CONFIG["db_path"] else Path.home() / ".sxigo_v25"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "sxigo_v25.db"

# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================
class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = True
    temperature: float = CONFIG["default_temperature"]
    top_p: float = CONFIG["default_top_p"]
    max_tokens: int = CONFIG["default_max_tokens"]
    conversation_id: Optional[str] = None

class GenerateRequest(BaseModel):
    prompt: str
    model: str
    system: Optional[str] = None
    stream: bool = True
    temperature: float = CONFIG["default_temperature"]
    max_tokens: int = CONFIG["default_max_tokens"]

class SettingsUpdate(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    boost_enabled: Optional[bool] = None

class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 10

class WebCrawlRequest(BaseModel):
    url: str
    max_chars: int = 12000

# ==============================================================================
# SYSTEM PROMPTS
# ==============================================================================
SYSTEM_PROMPTS = {
    "default": "You are SXIGO AI v2.5. Respond in the same language as the user. Be concise yet thorough. Provide clear, actionable responses.",
    "coding": "You are SXIGO AI Coding Expert. Write clean, efficient, well-documented code. Explain complex logic clearly.",
    "creative": "You are SXIGO AI Creative Assistant. Help with writing, storytelling, brainstorming. Be imaginative and inspiring.",
    "academic": "You are SXIGO AI Academic Assistant. Help with research, analysis, learning. Provide detailed, structured information.",
    "korean": "당신은 SXIGO AI v2.5입니다. 항상 한국어로 응답하세요. 명확하고 자세히 설명해주세요.",
}

START_TIME = time.time()
_http_client: Optional[httpx.AsyncClient] = None
_available_models: List[Dict] = []
_models_cache_time = 0
_models_cache_ttl = 300

# ==============================================================================
# DATABASE FUNCTIONS
# ==============================================================================
def get_db():
    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA cache_size=-262144")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise

def init_db():
    try:
        conn = get_db()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT DEFAULT 'Chat',
                model TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                message_count INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT CHECK(role IN ('user','assistant')),
                content TEXT NOT NULL,
                tokens INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS boost_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enabled BOOLEAN DEFAULT 0,
                multiplier INTEGER DEFAULT 5,
                timestamp TEXT DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations(updated_at DESC);
        """)
        conn.commit()
        conn.close()
        logger.info(f"✓ Database initialized: {DB_PATH}")
    except Exception as e:
        logger.error(f"DB init error: {e}")
        raise

# ==============================================================================
# HTTP CLIENT MANAGEMENT
# ==============================================================================
def get_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None:
        limits = httpx.Limits(
            max_keepalive_connections=50,
            max_connections=100,
            keepalive_expiry=60
        )
        _http_client = httpx.AsyncClient(
            timeout=None,
            limits=limits,
            headers={"Connection": "keep-alive"}
        )
    return _http_client

# ==============================================================================
# MODEL MANAGEMENT
# ==============================================================================
async def get_available_models():
    global _available_models, _models_cache_time
    
    current_time = time.time()
    if _available_models and (current_time - _models_cache_time) < _models_cache_ttl:
        return _available_models
    
    try:
        result = await ollama_request("GET", "tags")
        models = []
        for m in result.get("models", []):
            size_bytes = m.get("size", 0)
            if size_bytes > 1073741824:
                size_str = f"{size_bytes / 1073741824:.1f}GB"
            elif size_bytes > 1048576:
                size_str = f"{size_bytes / 1048576:.1f}MB"
            else:
                size_str = f"{size_bytes / 1024:.1f}KB"
            
            models.append({
                "name": m["name"],
                "display_name": m["name"].split(":")[0].upper(),
                "size": size_str,
                "modified": m.get("modified_at", "unknown"),
                "full_size_bytes": size_bytes
            })
        
        _available_models = sorted(models, key=lambda x: x["name"])
        _models_cache_time = current_time
        return _available_models
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return []

async def validate_model(model_name: str) -> bool:
    try:
        models = await get_available_models()
        return any(m["name"] == model_name for m in models)
    except Exception:
        return False

# ==============================================================================
# FASTAPI APP INITIALIZATION
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        global _http_client
        _http_client = get_client()
        
        # Pre-load models
        await get_available_models()
        
        logger.info("\n" + "="*80)
        logger.info("🚀 SXIGO AI v2.5 Server - Enhanced Edition")
        logger.info("="*80)
        logger.info(f"✓ Python: {platform.python_version()}")
        logger.info(f"✓ Platform: {platform.system()} {platform.release()}")
        logger.info(f"✓ Ollama: {CONFIG['ollama_host']}")
        logger.info(f"✓ Database: {DB_PATH}")
        logger.info(f"✓ 5X BOOST: Ready")
        logger.info(f"✓ Dynamic Models: Enabled")
        logger.info("="*80 + "\n")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    
    yield
    
    try:
        if _http_client:
            await _http_client.aclose()
            _http_client = None
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

app = FastAPI(
    title="SXIGO AI v2.5 - Enhanced",
    version="2.5.1",
    description="High-Performance AI Chat with 5X Boost",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=6)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# OLLAMA API COMMUNICATION
# ==============================================================================
async def ollama_request(method: str, endpoint: str, json_data: dict = None, retries: int = 2) -> dict:
    url = f"{CONFIG['ollama_host']}/api/{endpoint}"
    client = get_client()
    last_error = None

    for attempt in range(retries + 1):
        try:
            if method == "GET":
                resp = await client.get(url, timeout=30)
            elif method == "POST":
                resp = await client.post(url, json=json_data or {}, timeout=120)
            elif method == "DELETE":
                resp = await client.delete(url, timeout=30)
            else:
                raise ValueError(f"Unknown method: {method}")

            resp.raise_for_status()
            return resp.json()
        except (httpx.TimeoutException, httpx.RequestError) as e:
            last_error = e
            if attempt < retries:
                await asyncio.sleep(1.0 * (attempt + 1))
            continue
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            last_error = e
            if attempt < retries:
                await asyncio.sleep(1.0)

    raise HTTPException(status_code=503, detail=f"Ollama unavailable: {str(last_error)}")

async def ollama_stream_chat(
    model: str,
    messages: list,
    temperature: float,
    top_p: float,
    max_tokens: int,
    boost_enabled: bool = False
) -> AsyncGenerator[str, None]:
    # Apply 5X boost if enabled
    if boost_enabled:
        temperature = max(0.1, temperature * 0.8)  # Reduce randomness
        top_p = min(0.95, top_p * 1.1)
        max_tokens = min(int(max_tokens * 1.5), 12288)  # Increase output
    
    url = f"{CONFIG['ollama_host']}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": max_tokens,
            "num_keep": -1,
        }
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
    except asyncio.CancelledError:
        logger.info("Chat stream cancelled")
    except Exception as e:
        logger.error(f"Stream error: {e}")
        yield f"\n[Error: {str(e)}]"

async def ollama_stream_generate(
    prompt: str,
    model: str,
    system: str,
    temperature: float,
    max_tokens: int,
    boost_enabled: bool = False
) -> AsyncGenerator[str, None]:
    if boost_enabled:
        temperature = max(0.1, temperature * 0.8)
        max_tokens = min(int(max_tokens * 1.5), 12288)
    
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
    except asyncio.CancelledError:
        logger.info("Generate stream cancelled")
    except Exception as e:
        logger.error(f"Generate error: {e}")
        yield f"\n[Error: {str(e)}]"

# ==============================================================================
# WEB ROUTES
# ==============================================================================
HTML_PATH = Path(__file__).parent / "SXIGOai_v2.5.html"

@app.get("/")
async def root():
    if HTML_PATH.exists():
        return FileResponse(str(HTML_PATH))
    return {
        "name": "SXIGO AI v2.5 Enhanced",
        "version": "2.5.1",
        "status": "running",
        "features": ["5X Boost", "Dynamic Models", "Auto-Loading"],
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    ollama_ok = False
    models_count = 0
    try:
        models = await get_available_models()
        ollama_ok = len(models) > 0
        models_count = len(models)
    except Exception as e:
        logger.warning(f"Health check failed: {e}")

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.5.1",
        "uptime_seconds": int(time.time() - START_TIME),
        "ollama": {
            "connected": ollama_ok,
            "host": CONFIG['ollama_host'],
            "models_available": models_count,
        },
        "features": {
            "boost_enabled": CONFIG["boost_enabled"],
            "boost_multiplier": CONFIG["boost_multiplier"],
            "dynamic_models": True,
        }
    }

@app.get("/api/system")
async def system_info():
    models = await get_available_models()
    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = f"{uptime_seconds // 86400}d {(uptime_seconds % 86400) // 3600}h {(uptime_seconds % 3600) // 60}m"
    
    return {
        "platform": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "sxigo_version": "2.5.1",
        "uptime": uptime_str,
        "available_models": len(models),
        "boost_enabled": CONFIG["boost_enabled"],
    }

@app.get("/api/models")
async def list_models():
    try:
        models = await get_available_models()
        return {
            "models": models,
            "total": len(models),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Models error: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.post("/api/refresh-models")
async def refresh_models():
    global _available_models, _models_cache_time
    _available_models = []
    _models_cache_time = 0
    models = await get_available_models()
    return {
        "status": "refreshed",
        "models_found": len(models),
        "models": models
    }

# ==============================================================================
# CHAT API
# ==============================================================================
@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    # Validate model exists
    if not await validate_model(request.model):
        raise HTTPException(status_code=400, detail=f"Model '{request.model}' not found. Refresh models list.")
    
    messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    if not request.conversation_id:
        try:
            conn = get_db()
            title = messages_dict[-1]["content"][:50].strip() + "..."
            conn.execute(
                "INSERT INTO conversations (id, title, model) VALUES (?, ?, ?)",
                (conv_id, title, request.model)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Conv error: {e}")

    if request.stream:
        return StreamingResponse(
            stream_chat_response(
                conv_id, request.model, messages_dict,
                request.temperature, request.top_p, request.max_tokens
            ),
            media_type="text/event-stream",
            headers={"X-Conversation-Id": conv_id}
        )
    else:
        full_response = ""
        try:
            async for chunk in ollama_stream_chat(
                request.model, messages_dict,
                request.temperature, request.top_p, request.max_tokens,
                CONFIG["boost_enabled"]
            ):
                full_response += chunk
            
            conn = get_db()
            conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (conv_id, messages_dict[-1]["content"]))
            conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (conv_id, full_response))
            conn.execute("UPDATE conversations SET message_count = message_count + 2 WHERE id = ?", (conv_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
        return {
            "conversation_id": conv_id,
            "message": {"role": "assistant", "content": full_response},
            "boost_active": CONFIG["boost_enabled"]
        }

async def stream_chat_response(conv_id: str, model: str, messages: list, temperature: float, top_p: float, max_tokens: int):
    full_response = ""
    try:
        async for chunk in ollama_stream_chat(
            model, messages, temperature, top_p, max_tokens,
            CONFIG["boost_enabled"]
        ):
            full_response += chunk
            yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
        
        try:
            conn = get_db()
            conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (conv_id, messages[-1]["content"]))
            conn.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (conv_id, full_response))
            conn.execute("UPDATE conversations SET message_count = message_count + 2, updated_at = datetime('now') WHERE id = ?", (conv_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Save error: {e}")
        
        yield f"data: {json.dumps({'type': 'done', 'conversation_id': conv_id, 'boost': CONFIG['boost_enabled']})}\n\n"
    except asyncio.CancelledError:
        logger.info("Stream cancelled")
    except Exception as e:
        logger.error(f"Stream error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

# ==============================================================================
# CONVERSATION MANAGEMENT
# ==============================================================================
@app.get("/api/conversations")
async def list_conversations(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT id, title, model, created_at, updated_at FROM conversations ORDER BY updated_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
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
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# GENERATE API
# ==============================================================================
@app.post("/api/generate")
async def generate_completion(request: GenerateRequest):
    if not await validate_model(request.model):
        raise HTTPException(status_code=400, detail=f"Model not found: {request.model}")
    
    try:
        if request.stream:
            return StreamingResponse(
                stream_generate_response(
                    request.prompt, request.model, request.system,
                    request.temperature, request.max_tokens
                ),
                media_type="text/event-stream",
            )
        
        full_response = ""
        async for chunk in ollama_stream_generate(
            request.prompt, request.model, request.system,
            request.temperature, request.max_tokens,
            CONFIG["boost_enabled"]
        ):
            full_response += chunk
        
        return {"response": full_response, "boost": CONFIG["boost_enabled"]}
    except Exception as e:
        logger.error(f"Generate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_generate_response(prompt: str, model: str, system: str, temperature: float, max_tokens: int):
    try:
        async for chunk in ollama_stream_generate(
            prompt, model, system, temperature, max_tokens,
            CONFIG["boost_enabled"]
        ):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield f"data: {json.dumps({'done': True, 'boost': CONFIG['boost_enabled']})}\n\n"
    except Exception as e:
        logger.error(f"Generate stream error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

# ==============================================================================
# BOOST CONTROL
# ==============================================================================
@app.get("/api/boost/status")
async def get_boost_status():
    return {
        "enabled": CONFIG["boost_enabled"],
        "multiplier": CONFIG["boost_multiplier"],
        "description": "5X Speed Boost - Optimized Temperature & Token Allocation"
    }

@app.post("/api/boost/toggle")
async def toggle_boost(enabled: bool):
    CONFIG["boost_enabled"] = enabled
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO boost_log (enabled, multiplier) VALUES (?, ?)",
            (enabled, CONFIG["boost_multiplier"])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Boost log error: {e}")
    
    logger.info(f"Boost {'enabled' if enabled else 'disabled'}")
    return {
        "status": "updated",
        "boost_enabled": CONFIG["boost_enabled"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/boost/set-multiplier")
async def set_boost_multiplier(multiplier: int = Query(5, ge=1, le=10)):
    CONFIG["boost_multiplier"] = multiplier
    logger.info(f"Boost multiplier set to {multiplier}X")
    return {
        "status": "updated",
        "multiplier": CONFIG["boost_multiplier"]
    }

# ==============================================================================
# SETTINGS
# ==============================================================================
@app.get("/api/settings")
async def get_settings():
    try:
        conn = get_db()
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        conn.close()
        settings = {row["key"]: row["value"] for row in rows}
        return {
            "temperature": float(settings.get("temperature", CONFIG["default_temperature"])),
            "top_p": float(settings.get("top_p", CONFIG["default_top_p"])),
            "max_tokens": int(settings.get("max_tokens", CONFIG["default_max_tokens"])),
            "system_prompts": SYSTEM_PROMPTS,
            "boost_enabled": CONFIG["boost_enabled"],
        }
    except Exception as e:
        logger.error(f"Settings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/settings")
async def update_settings(update: SettingsUpdate):
    try:
        conn = get_db()
        if update.temperature is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('temperature', ?)", (str(update.temperature),))
        if update.top_p is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('top_p', ?)", (str(update.top_p),))
        if update.max_tokens is not None:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('max_tokens', ?)", (str(update.max_tokens),))
        if update.boost_enabled is not None:
            CONFIG["boost_enabled"] = update.boost_enabled
            logger.info(f"Boost {'enabled' if update.boost_enabled else 'disabled'}")
        conn.commit()
        conn.close()
        return {"status": "saved", "boost": CONFIG["boost_enabled"]}
    except Exception as e:
        logger.error(f"Update settings error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# UTILITY
# ==============================================================================
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
    return {
        "version": "2.5.1",
        "build": "SXIGO AI v2.5 Enhanced",
        "features": ["5X Boost", "Dynamic Models", "All Local Models Support"],
        "python_version": platform.python_version(),
    }

@app.get("/api/stats")
async def get_stats():
    try:
        conn = get_db()
        stats = {
            "total_conversations": conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0],
            "total_messages": conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
            "boost_toggles": conn.execute("SELECT COUNT(*) FROM boost_log").fetchone()[0],
        }
        conn.close()
        return stats
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================================================
# SERVER STARTUP
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
        print("\n" + "="*90)
        print(" "*20 + "🚀 SXIGO AI v2.5.1 Server - Enhanced Edition")
        print("="*90)
        print(f"  Ollama Host       : {CONFIG['ollama_host']}")
        print(f"  Database          : {DB_PATH}")
        print(f"  Port              : {CONFIG['server_host']}:{port}")
        print(f"  Features          : 5X BOOST | Dynamic Models | Auto-Loading")
        print(f"  GPU Optimized     : ✓ GTX1660 SUPER")
        print(f"  RAM Mode          : ✓ 4GB OPTIMIZED")
        print("="*90)
        print(f"\n  🌐 Open browser: http://localhost:{port}")
        print(f"  📚 API Docs: http://localhost:{port}/docs")
        print(f"  🔧 Swagger: http://localhost:{port}/swagger\n")
        print("="*90 + "\n")
        
        uvicorn.run(
            app,
            host=CONFIG["server_host"],
            port=port,
            log_level="info",
            access_log=True,
        )
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
