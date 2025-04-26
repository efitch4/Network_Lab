import os
import re
import threading
import sqlite3
import subprocess
from tkinter import Tk, Text, Button, Entry, Label, END
from datetime import datetime
from pathlib import Path

def is_valid_ip(ip):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return re.match(pattern, ip) is not None and all(0 <= int(octet) <= 255 for octet in ip.split('.'))

class PingLogger:
    def __init__(self, db_name="ping_results.db"):
        self.db_name = db_name
        self.setup()

    def setup(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    ip TEXT,
                    status TEXT,
                    timestamp TIMESTAMP
                )
            """)

    def log(self, ip, status):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO results (ip, status, timestamp) VALUES (?, ?, ?)",
                (ip, status, datetime.now())
            )

class NetworkScanner:
    def __init__(self, logger):
        self.logger = logger
        self.reachable = []

    def ping(self, ip, output_func):
        try:
            response = subprocess.run(["ping", "-n" if os.name == "nt" else "-c", "1", ip],
                                      stdout=subprocess.DEVNULL)
            status = "Reachable" if response.returncode == 0 else "Unreachable"
            self.logger.log(ip, status)
            output_func(f"{ip} is {status}")
            if status == "Reachable":
                self.reachable.append(ip)
        except Exception as e:
            output_func(f"Error pinging {ip}: {e}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Ping Sweep Tool")
        self.output = Text(root, width=80, height=25)
        self.output.pack()

        Label(root, text="Base IP (e.g., 192.168.1.)").pack()
        self.entry = Entry(root)
        self.entry.pack()

        Button(root, text="Start Ping Sweep", command=self.start_sweep).pack()
        Button(root, text="Clear Output", command=self.clear_output).pack()

        self.logger = PingLogger()
        self.scanner = NetworkScanner(self.logger)

    def write(self, message):
        self.output.insert(END, message + "\n")
        self.output.see(END)

    def clear_output(self):
        self.output.delete(1.0, END)

    def start_sweep(self):
        base_ip = self.entry.get().strip()
        if not base_ip or not is_valid_ip(base_ip + "1"):
            self.write("Invalid base IP. Try something like 192.168.1.")
            return
        threads = []
        self.write(f"Starting ping sweep on {base_ip}0-254...")
        for i in range(1, 255):
            ip = f"{base_ip}{i}"
            t = threading.Thread(target=self.scanner.ping, args=(ip, self.write))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
        self.write("Ping sweep complete.")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

