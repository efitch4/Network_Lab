import os
import hashlib
import socket
import re
import shutil
import argparse
from cryptography.fernet import Fernet
from datetime import datetime

# ------------------ File Hasher Class ------------------ #
class FileHasher:
    def __init__(self, algorithm="sha256"):
        self.algorithm = algorithm

    def hash_file(self, filepath):
        try:
            with open(filepath, "rb") as f:
                file_data = f.read()
            if self.algorithm == "sha256":
                return hashlib.sha256(file_data).hexdigest()
            elif self.algorithm == "md5":
                return hashlib.md5(file_data).hexdigest()
            else:
                raise ValueError("Unsupported hashing algorithm.")
        except Exception as e:
            print(f"[!] Error hashing {filepath}: {e}")
            return None

    def hash_directory(self, directory):
        hashes = {}
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                file_hash = self.hash_file(path)
                if file_hash:
                    hashes[path] = file_hash
        return hashes

# ------------------ File Encryptor Class ------------------ #
class FileEncryptor:
    def __init__(self, key_path="secret.key"):
        self.key_path = key_path
        self.key = self.load_or_create_key()

    def load_or_create_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            print("[+] New encryption key generated.")
        else:
            key = open(self.key_path, "rb").read()
        return key

    def encrypt_file(self, file_path):
        fernet = Fernet(self.key)
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted = fernet.encrypt(data)
        with open(file_path + ".enc", "wb") as file:
            file.write(encrypted)
        print(f"[+] Encrypted: {file_path}")

    def decrypt_file(self, enc_path):
        fernet = Fernet(self.key)
        with open(enc_path, "rb") as file:
            data = file.read()
        decrypted = fernet.decrypt(data)
        orig_path = enc_path.replace(".enc", "")
        with open(orig_path, "wb") as file:
            file.write(decrypted)
        print(f"[+] Decrypted: {orig_path}")

# ------------------ Secure File Deletion ------------------ #
def secure_delete(file_path):
    if os.path.exists(file_path):
        with open(file_path, "ba+") as file:
            length = file.tell()
        with open(file_path, "br+") as file:
            file.write(os.urandom(length))
        os.remove(file_path)
        print(f"[+] Securely deleted {file_path}")
    else:
        print("[!] File not found for secure deletion.")

# ------------------ Port Scanner ------------------ #
def scan_ports(ip, ports):
    print(f"[+] Scanning {ip} for ports: {ports}")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"  [OPEN] Port {port}")
            sock.close()
        except Exception as e:
            print(f"  [ERROR] {e}")

# ------------------ Password Strength Checker ------------------ #
def is_strong_password(password):
    length = len(password) >= 12
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    digit = re.search(r"\d", password)
    special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    return all([length, upper, lower, digit, special])

# ------------------ Log Analysis ------------------ #
def detect_suspicious_ips(log_file):
    suspicious_ips = set()
    try:
        with open(log_file, "r") as file:
            for line in file:
                if "Failed login" in line or "error" in line.lower():
                    match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
                    if match:
                        suspicious_ips.add(match.group())
    except Exception as e:
        print(f"[!] Error reading log file: {e}")
    return suspicious_ips

# ------------------ Input Sanitization ------------------ #
def sanitize_input(user_input):
    return re.sub(r"[^\w\s]", "", user_input)

# ------------------ Argument Parser ------------------ #
def create_arg_parser():
    parser = argparse.ArgumentParser(description="Advanced Security+ Toolkit")
    parser.add_argument("--scan", metavar="IP", help="Scan ports on a given IP")
    parser.add_argument("--ports", metavar="P", nargs="+", type=int, default=[22, 80, 443], help="Ports to scan")
    parser.add_argument("--hashfile", metavar="FILE", help="Hash a single file")
    parser.add_argument("--hashdir", metavar="DIR", help="Hash all files in a directory")
    parser.add_argument("--encrypt", metavar="FILE", help="Encrypt a file")
    parser.add_argument("--decrypt", metavar="ENCFILE", help="Decrypt a file")
    parser.add_argument("--delete", metavar="FILE", help="Securely delete a file")
    parser.add_argument("--checkpass", metavar="PASS", help="Check password strength")
    parser.add_argument("--logscan", metavar="LOGFILE", help="Scan log file for suspicious IPs")
    parser.add_argument("--sanitize", metavar="STRING", help="Sanitize user input")
    return parser

# ------------------ Main Driver ------------------ #
if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()

    hasher = FileHasher()
    encryptor = FileEncryptor()

    if args.scan:
        scan_ports(args.scan, args.ports)

    if args.hashfile:
        file_hash = hasher.hash_file(args.hashfile)
        if file_hash:
            print(f"[+] Hash: {file_hash}")

    if args.hashdir:
        hashes = hasher.hash_directory(args.hashdir)
        for path, file_hash in hashes.items():
            print(f"{path}: {file_hash}")

    if args.encrypt:
        encryptor.encrypt_file(args.encrypt)

    if args.decrypt:
        encryptor.decrypt_file(args.decrypt)

    if args.delete:
        secure_delete(args.delete)

    if args.checkpass:
        if is_strong_password(args.checkpass):
            print("[+] Password is strong.")
        else:
            print("[!] Password is weak.")

    if args.logscan:
        suspicious = detect_suspicious_ips(args.logscan)
        if suspicious:
            for ip in suspicious:
                print(f"[ALERT] Suspicious IP: {ip}")
        else:
            print("[+] No suspicious activity detected.")

    if args.sanitize:
        clean = sanitize_input(args.sanitize)
        print(f"[+] Sanitized: {clean}")

