# Install needed libraries first:
# pip install fastapi uvicorn cryptography

import os
import re
import hashlib
import socket
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from typing import List, Optional
from pathlib import Path

app = FastAPI()

# --------------- Models --------------- #
class PortScanRequest(BaseModel):
    ip: str
    ports: List[int]

class HashFileRequest(BaseModel):
    filepath: str

class EncryptFileRequest(BaseModel):
    filepath: str

class DecryptFileRequest(BaseModel):
    enc_filepath: str

class PasswordStrengthRequest(BaseModel):
    password: str

class LogScanRequest(BaseModel):
    log_path: str

class SanitizeInputRequest(BaseModel):
    user_input: str

# --------------- Services --------------- #

# --- Hashing Service --- #
class FileHasher:
    def __init__(self, algorithm: str = "sha256"):
        self.algorithm = algorithm

    def hash_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found.")
        with open(filepath, "rb") as f:
            file_data = f.read()
            if self.algorithm == "sha256":
                return hashlib.sha256(file_data).hexdigest()
            elif self.algorithm == "md5":
                return hashlib.md5(file_data).hexdigest()
            else:
                raise ValueError("Unsupported hashing algorithm.")

# --- Encryption Service --- #
class FileEncryptor:
    def __init__(self, key_path: str = "secret.key"):
        self.key_path = key_path
        self.key = self._load_or_generate_key()

    def _load_or_generate_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)
        else:
            key = open(self.key_path, "rb").read()
        return key

    def encrypt_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found.")
        fernet = Fernet(self.key)
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        encrypted_path = filepath + ".enc"
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)
        return encrypted_path

    def decrypt_file(self, enc_filepath: str) -> str:
        if not os.path.exists(enc_filepath):
            raise FileNotFoundError(f"{enc_filepath} not found.")
        fernet = Fernet(self.key)
        with open(enc_filepath, "rb") as f:
            data = f.read()
        decrypted = fernet.decrypt(data)
        orig_filepath = enc_filepath.replace(".enc", "")
        with open(orig_filepath, "wb") as f:
            f.write(decrypted)
        return orig_filepath

# --- Port Scanner Service --- #
class PortScanner:
    async def scan_port(self, ip: str, port: int) -> Optional[int]:
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(1)
            result = conn.connect_ex((ip, port))
            conn.close()
            if result == 0:
                return port
        except:
            return None

    async def scan_ports(self, ip: str, ports: List[int]) -> List[int]:
        tasks = [self.scan_port(ip, port) for port in ports]
        results = await asyncio.gather(*tasks)
        return [port for port in results if port is not None]

# --- Log Scanner Service --- #
class LogAnalyzer:
    def find_suspicious_ips(self, log_path: str) -> List[str]:
        suspicious_ips = []
        if not os.path.exists(log_path):
            raise FileNotFoundError(f"{log_path} not found.")
        with open(log_path, "r") as file:
            for line in file:
                if "failed login" in line.lower() or "error" in line.lower():
                    match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
                    if match:
                        suspicious_ips.append(match.group())
        return suspicious_ips

# --- Password Strength Checker --- #
def is_strong_password(password: str) -> bool:
    length = len(password) >= 12
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    digit = re.search(r"\d", password)
    special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    return all([length, upper, lower, digit, special])

# --- Input Sanitizer --- #
def sanitize_input(user_input: str) -> str:
    return re.sub(r"[^\w\s]", "", user_input)

# --------------- Dependency Injection --------------- #
hasher = FileHasher()
encryptor = FileEncryptor()
scanner = PortScanner()
log_analyzer = LogAnalyzer()

# --------------- API Endpoints --------------- #

@app.post("/hash")
async def hash_file(req: HashFileRequest):
    try:
        file_hash = hasher.hash_file(req.filepath)
        return {"filepath": req.filepath, "hash": file_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/encrypt")
async def encrypt_file(req: EncryptFileRequest):
    try:
        encrypted_path = encryptor.encrypt_file(req.filepath)
        return {"message": f"File encrypted at {encrypted_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decrypt")
async def decrypt_file(req: DecryptFileRequest):
    try:
        decrypted_path = encryptor.decrypt_file(req.enc_filepath)
        return {"message": f"File decrypted to {decrypted_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/scan_ports")
async def scan_ports(req: PortScanRequest):
    try:
        open_ports = await scanner.scan_ports(req.ip, req.ports)
        return {"open_ports": open_ports}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/check_password")
async def check_password(req: PasswordStrengthRequest):
    if is_strong_password(req.password):
        return {"result": "Strong Password"}
    else:
        return {"result": "Weak Password"}

@app.post("/scan_log")
async def scan_log(req: LogScanRequest):
    try:
        suspicious_ips = log_analyzer.find_suspicious_ips(req.log_path)
        return {"suspicious_ips": suspicious_ips}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sanitize")
async def sanitize(req: SanitizeInputRequest):
    sanitized = sanitize_input(req.user_input)
    return {"sanitized_input": sanitized}
