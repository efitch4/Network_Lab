import os 
import re
import hashlib
import socket
import asyncio
from fastapi import FastAPI,UploadFile, File, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from typing import List, Optional
from pathlib import Path

app = FastAPI

class PortScanRequest(BaseModel):
    ip: str
    ports: List[int]

class HashFileRequest(BaseModel):
    filepath: str 

class EncryptFileRequest(BaseModel):
    filepath: str

class DecryptFileEquest(BaseModel):
    filepath: str

class DecryptFileRequest(BaseModel):
    end_filepath: str

class PasswordStrengthRequest(BaseModel):
    password: str

class LogScanRequest(BaseModel):
    log_path: str

class SanitizeInputRequest(BaseModel):
    user_input: str


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
                raise ValueError("Unsupported hashing algorithm")
            
    