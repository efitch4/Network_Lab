# Part 3: Advanced Python Drill with FastAPI, Async, Pydantic, Modular Structure

import os
import re
import aiohttp
import sqlite3
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# --- SQLite Logging ---
class ScanLogger:
    def __init__(self, db_name="scan_log.db"):
        self.db_name = db_name
        self.setup()

    def setup(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    file TEXT,
                    status TEXT,
                    time TIMESTAMP
                )
            """)

    def log(self, file_path: str, status: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO logs (file, status, time) VALUES (?, ?, ?)",
                (file_path, status, datetime.now())
            )

    def fetch_all(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM logs")
            return cur.fetchall()

# --- File Scanning ---
def get_all_files(directory: str, extensions: tuple):
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files if file.lower().endswith(extensions)
    ]

def safe_get_size_kb(file_path: str):
    try:
        return os.path.getsize(file_path) / 1024
    except Exception:
        return 0

class FileScanner:
    def __init__(self, min_size_kb=100, extensions=(".mp4", ".mkv", ".avi")):
        self.min_size_kb = min_size_kb
        self.extensions = extensions

    def scan(self, folder: str):
        valid_files = []
        files = get_all_files(folder, self.extensions)
        for f in files:
            size_kb = safe_get_size_kb(f)
            if size_kb >= self.min_size_kb:
                valid_files.append(f)
        return valid_files

# --- Async Quote Fetching ---
async def get_random_quote():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random", timeout=5) as res:
                data = await res.json()
                return {"quote": data["content"], "author": data["author"]}
    except:
        return {"quote": "Failed to fetch quote.", "author": "Unknown"}

# --- Pydantic Models ---
class ScanRequest(BaseModel):
    folder_path: str
    min_size_kb: Optional[int] = 100
    extensions: Optional[List[str]] = [".mp4", ".mkv", ".avi"]

class ScanResult(BaseModel):
    valid_files: List[str]
    total: int

class LogEntry(BaseModel):
    id: int
    file: str
    status: str
    time: str

# --- FastAPI Setup ---
app = FastAPI()
logger = ScanLogger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI Backend Running"}

@app.post("/scan", response_model=ScanResult)
def scan_files(req: ScanRequest):
    if not os.path.isdir(req.folder_path):
        raise HTTPException(status_code=400, detail="Invalid folder path")
    scanner = FileScanner(min_size_kb=req.min_size_kb, extensions=tuple(req.extensions))
    valid_files = scanner.scan(req.folder_path)
    for f in valid_files:
        logger.log(f, "VALID")
    return ScanResult(valid_files=valid_files, total=len(valid_files))

@app.get("/logs", response_model=List[LogEntry])
def get_logs():
    entries = logger.fetch_all()
    return [LogEntry(id=row[0], file=row[1], status=row[2], time=row[3]) for row in entries]

@app.get("/quote")
async def fetch_quote():
    result = await get_random_quote()
    return JSONResponse(content=result)

@app.get("/regex")
def regex_demo():
    text = "An awesome apple always attracts attention."
    matches = re.findall(r"\\ba\\w*", text, re.IGNORECASE)
    return {"matches": matches}

@app.get("/example-dog")
def dog_example():
    class Dog:
        def __init__(self, name, breed):
            self.name = name
            self.breed = breed
        def bark(self):
            return f"{self.name} the {self.breed} says Woof!"

    d = Dog("Rex", "Labrador")
    return {"message": d.bark()}

@app.get("/error-demo")
def error_example():
    try:
        result = 10 / 0
    except ZeroDivisionError:
        return {"error": "Caught division by zero error."}
    return {"result": result}
