import socket
import re
import hashlib
import os
from cryptography.fernet import Fernet
from datetime import datetime

# ------------------ Port Scanner ------------------ #
def scan_ports(target_ip, ports):
    print(f"[+] Scanning {target_ip}")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
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

# ------------------ Log Analyzer ------------------ #
def detect_suspicious_ips(log_file):
    print("[+] Scanning logs for suspicious IPs...")
    with open(log_file, "r") as file:
        for line in file:
            if "Failed login" in line:
                match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
                if match:
                    print(f"  [ALERT] Suspicious IP: {match.group()}")

# ------------------ File Integrity Check ------------------ #
def hash_file(filepath):
    with open(filepath, "rb") as f:
        file_data = f.read()
        return hashlib.sha256(file_data).hexdigest()

# ------------------ File Encryption / Decryption ------------------ #
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("[+] Key generated.")

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    f = Fernet(key)
    encrypted = f.encrypt(data)
    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted)
    print(f"[+] Encrypted: {file_path}")

def decrypt_file(enc_path, key):
    with open(enc_path, "rb") as file:
        data = file.read()
    f = Fernet(key)
    decrypted = f.decrypt(data)
    orig_path = enc_path.replace(".enc", "")
    with open(orig_path, "wb") as file:
        file.write(decrypted)
    print(f"[+] Decrypted: {orig_path}")

# ------------------ Input Sanitization ------------------ #
def sanitize_input(user_input):
    # Remove anything that's not alphanumeric or space
    return re.sub(r"[^\w\s]", "", user_input)

# ------------------ Main Execution ------------------ #
if __name__ == "__main__":
    print("=== Security+ Drill ===\n")

    # 1. Scan common ports
    scan_ports("127.0.0.1", [21, 22, 23, 80, 443, 3389])

    # 2. Check password strength
    password = input("\nEnter a password to check: ")
    if is_strong_password(password):
        print("[+] Strong password.")
    else:
        print("[!] Weak password.")

    # 3. Analyze a sample log file
    sample_log = "auth.log"
    if os.path.exists(sample_log):
        detect_suspicious_ips(sample_log)
    else:
        print("[!] Sample log file not found.")

    # 4. Check file integrity
    test_file = "example.txt"
    if os.path.exists(test_file):
        print(f"[+] File Hash: {hash_file(test_file)}")
    else:
        print("[!] example.txt not found.")

    # 5. Encrypt/decrypt example.txt
    if not os.path.exists("secret.key"):
        generate_key()
    key = load_key()
    if os.path.exists(test_file):
        encrypt_file(test_file, key)
        decrypt_file(test_file + ".enc", key)

    # 6. Sanitize input
    user_command = input("\nEnter a shell command (sanitized): ")
    clean = sanitize_input(user_command)
    print(f"[+] Sanitized Input: {clean}")
