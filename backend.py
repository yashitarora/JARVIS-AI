"""JARVIS AI - Complete Backend Server."""
import asyncio
import json
import logging
import os
import subprocess
import platform
import random
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ============================================================
# Initialize FastAPI App
# ============================================================
app = FastAPI(title="JARVIS AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Data Models
# ============================================================
class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None

class CommandRequest(BaseModel):
    command: str
    args: Optional[Dict[str, Any]] = {}

# ============================================================
# Health Check
# ============================================================
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "2.0.0"}

# ============================================================
# Local Command Endpoint
# ============================================================
@app.post("/api/local/command")
async def local_command(request: CommandRequest):
    cmd = request.command.lower().strip()

    # Time
    if cmd in ["what time", "time", "what is the time", "tell me the time", "current time"]:
        now = datetime.now()
        return {"response": f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}", "type": "time"}

    # Date
    if cmd in ["what date", "date", "what is the date", "today's date", "today"]:
        now = datetime.now()
        return {"response": f"Today is {now.strftime('%A, %B %d, %Y')}", "type": "date"}

    # Jokes
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
        "What's a computer's favorite snack? Microchips!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "What do you call a computer that sings? A-Dell!",
        "Why do Java developers wear glasses? Because they can't C#!",
        "How does a computer get drunk? It takes screenshots!",
        "Why was the computer cold? It left its Windows open!",
        "There are only 10 types of people in the world: those who understand binary and those who don't.",
        "A SQL query walks into a bar, sees two tables and asks: Can I join you?",
    ]
    if cmd in ["joke", "tell me a joke", "say a joke", "funny", "make me laugh"]:
        return {"response": random.choice(jokes), "type": "joke"}

    # System info
    if cmd in ["system", "system info", "computer info", "what are my specs"]:
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        }
        return {"response": f"OS: {info['os']} {info['os_version']}\nMachine: {info['machine']}\nProcessor: {info['processor']}", "type": "system"}

    # Help
    if cmd in ["help", "what can you do", "commands", "command list"]:
        return {"response": "I can:\n- Open apps: 'open whatsapp'\n- Open folders: 'open documents'\n- Tell time: 'what time'\n- Tell jokes: 'tell me a joke'\n- System info: 'system'\n- Search files: 'find [filename]'\n- Volume control: 'volume up/down'\n- WiFi control: 'wifi on/off'\n- Call: 'call [contact]'\n- Message: 'message [contact]'", "type": "help"}

    # Find files
    if cmd.startswith("find ") or cmd.startswith("search ") or cmd.startswith("look for "):
        query = cmd.replace("find ", "").replace("search ", "").replace("look for ", "").strip()
        return await find_files(query)

    # Open file/folder
    if cmd.startswith("open "):
        target = cmd[5:].strip()
        return await open_file_or_folder(target)

    return None


async def open_file_or_folder(target: str):
    home = Path.home()
    common_dirs = [
        home / "Desktop", home / "Documents", home / "Downloads",
        home / "Pictures", home / "Movies", home / "Music", home,
    ]

    for d in common_dirs:
        if (d / target).exists():
            path = str(d / target)
            subprocess.Popen(["open", path])
            return {"response": f"Opening {target}", "type": "open", "path": path}

        matches = list(d.glob(f"*{target}*"))
        if matches:
            path = str(matches[0])
            subprocess.Popen(["open", path])
            return {"response": f"Opening {matches[0].name}", "type": "open", "path": path}

    try:
        for p in home.rglob(f"*{target}*"):
            if p.is_file() or p.is_dir():
                path = str(p)
                subprocess.Popen(["open", path])
                return {"response": f"Opening {p.name}", "type": "open", "path": path}
    except PermissionError:
        pass

    return {"response": f"Could not find '{target}' on your system.", "type": "error"}


async def find_files(query: str):
    home = Path.home()
    results = []
    try:
        for p in home.rglob(f"*{query}*"):
            if len(results) >= 10:
                break
            results.append({"name": p.name, "path": str(p), "type": "dir" if p.is_dir() else "file"})
    except PermissionError:
        pass

    if results:
        files_list = "\n".join([f"[{'DIR' if r['type']=='dir' else 'FILE'}] {r['name']}" for r in results])
        return {"response": f"Found:\n{files_list}", "type": "search", "results": results}
    return {"response": f"No files found matching '{query}'", "type": "search", "results": []}


# ============================================================
# System Command Endpoint
# ============================================================
@app.post("/api/system/command")
async def execute_command(request: CommandRequest):
    try:
        result = subprocess.run(
            request.command, shell=True, capture_output=True, text=True, timeout=30
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}


# ============================================================
# System Stats
# ============================================================
@app.get("/api/system/stats")
async def system_stats():
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        return {"cpu_percent": cpu, "memory_percent": mem.percent, "memory_total": mem.total, "memory_used": mem.used}
    except ImportError:
        # Fallback: use subprocess
        try:
            cpu_result = subprocess.run(
                "top -l 1 | grep 'CPU usage' | awk '{print $3}' | sed 's/%//'",
                shell=True, capture_output=True, text=True, timeout=5
            )
            cpu = float(cpu_result.stdout.strip()) if cpu_result.stdout.strip() else 20.0
            return {"cpu_percent": cpu, "memory_percent": 55.0, "memory_total": 8000000000, "memory_used": 4400000000}
        except:
            return {"cpu_percent": 20.0, "memory_percent": 55.0}


# ============================================================
# Chat Endpoint (simple echo for now)
# ============================================================
@app.post("/api/chat")
async def chat(request: ChatRequest):
    msg = request.message.lower()

    # Simple pattern matching responses
    if "hello" in msg or "hi" in msg or "hey" in msg:
        response = "Hello! I am JARVIS, your personal AI assistant. How can I help you?"
    elif "how are you" in msg:
        response = "I am doing well, thank you for asking! All systems are operational."
    elif "who are you" in msg or "your name" in msg:
        response = "I am JARVIS, Just A Rather Very Intelligent System. I am your personal AI assistant!"
    elif "who made you" in msg or "who created you" in msg:
        response = "I was created by Yash, a talented developer!"
    elif "thank" in msg:
        response = "You are welcome! Always happy to help."
    elif "weather" in msg:
        response = "I can check weather for you. What city are you in?"
    elif "time" in msg:
        now = datetime.now()
        response = f"It is {now.strftime('%I:%M %p')}"
    elif "date" in msg or "today" in msg:
        now = datetime.now()
        response = f"Today is {now.strftime('%A, %B %d, %Y')}"
    elif "joke" in msg:
        jokes = [
            "Why do programmers prefer dark mode? Light attracts bugs!",
            "Why was the JS dev sad? Could not Node how to Express himself!",
            "What is a computer's favorite snack? Microchips!",
            "Why did the computer go to the doctor? It had a virus!",
        ]
        response = random.choice(jokes)
    elif "open" in msg:
        target = msg.replace("open", "").strip()
        result = await open_file_or_folder(target)
        response = result.get("response", f"Opening {target}")
    elif "help" in msg:
        response = "I can help you with:\n- Opening apps and files\n- Telling time and jokes\n- System information\n- Searching files\n- And much more! Say 'help' for the full list."
    else:
        response = f"I understand you said: '{request.message}'. I am still learning. Try saying 'help' for available commands."

    return {
        "response": response,
        "provider": "local",
        "model": "jarvis-v2",
        "latency_ms": 0.1,
        "usage": {"prompt_tokens": 0, "completion_tokens": 0}
    }


# ============================================================
# WebSocket
# ============================================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "chat":
                user_message = message.get("content", "")
                # Simple local response
                if "hello" in user_message.lower() or "hi" in user_message.lower():
                    response = "Hello! How can I help you?"
                elif "time" in user_message.lower():
                    response = f"It is {datetime.now().strftime('%I:%M %p')}"
                elif "joke" in user_message.lower():
                    response = random.choice(["Why do programmers prefer dark mode? Light attracts bugs!", "What is a computer's favorite snack? Microchips!"])
                else:
                    response = f"I heard: '{user_message}'. Try saying 'help' for commands."

                await websocket.send_json({"type": "stream", "content": response})
                await websocket.send_json({"type": "complete", "content": response})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logging.error(f"WebSocket error: {e}")


# ============================================================
# Serve the frontend
# ============================================================
@app.get("/")
async def serve_index():
    from fastapi.responses import FileResponse
    return FileResponse(Path(__file__).parent / "jarvis.html")

@app.get("/jarvis.html")
async def serve_jarvis():
    from fastapi.responses import FileResponse
    return FileResponse(Path(__file__).parent / "jarvis.html")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    import uvicorn
    print("JARVIS AI Backend starting on port 8000...")
    print("Frontend: http://localhost:8000/jarvis.html")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
