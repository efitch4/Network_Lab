import os
import json
import re
import random
import sqlite3
import threading
import requests
from pathlib import Path
from tkinter import Tk, Button, Label, Text, filedialog, END
from bs4 import BeautifulSoup
from datetime import datetime

# -------------------------------
# SECTION 1: Utilities
# -------------------------------
def get_all_files(directory, extensions):
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files if file.lower().endswith(extensions)
    ]

def safe_get_size_kb(file_path):
    try:
        return os.path.getsize(file_path) / 1024
    except Exception as e:
        return 0

def get_random_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=5)
        data = res.json()
        return f'"{data["content"]}" - {data["author"]}'
    except:
        return "Failed to fetch quote."

def scrape_articles():
    try:
        response = requests.get("https://realpython.github.io/fake-tasks/")
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="card-content")[:3]
        return [f"{a.find('h2').text.strip()} by {a.find('h3').text.strip()}" for a in articles]
    except:
        return ["Could not scrape articles."]

# -------------------------------
# SECTION 2: Scanner + Logger
# -------------------------------
class FileScanner:
    def __init__(self, min_size_kb=100, extensions=(".mp4", ".mkv", ".avi")):
        self.min_size_kb = min_size_kb
        self.extensions = extensions
        self.valid_files = []

    def validate_file(self, file_path):
        size_kb = safe_get_size_kb(file_path)
        if size_kb >= self.min_size_kb:
            self.valid_files.append(file_path)
            return True
        return False

    def scan(self, folder):
        files = get_all_files(folder, self.extensions)
        for f in files:
            self.validate_file(f)
        return self.valid_files

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

    def log(self, file_path, status):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO logs (file, status, time) VALUES (?, ?, ?)",
                (file_path, status, datetime.now())
            )

# -------------------------------
# SECTION 3: The GUI App
# -------------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Python Syntax Drill")
        self.text = Text(root, width=100, height=25)
        self.text.pack(pady=10)

        Button(root, text=" Scan Media Folder", command=self.scan_folder).pack()
        Button(root, text=" Show Random Quote", command=self.display_quote).pack()
        Button(root, text=" Scrape Python Articles", command=self.display_articles).pack()
        Button(root, text=" List Directory & Read sample.txt", command=self.read_files).pack()
        Button(root, text=" Run Mini Syntax Examples", command=self.run_examples).pack()

        self.scanner = FileScanner()
        self.logger = ScanLogger()

    def write(self, msg):
        self.text.insert(END, msg + "\n")
        self.text.see(END)

    def scan_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            thread = threading.Thread(target=self._scan_worker, args=(folder,))
            thread.start()

    def _scan_worker(self, folder):
        valid_files = self.scanner.scan(folder)
        for file in valid_files:
            self.logger.log(file, "VALID")
        self.write(f" Scan complete. {len(valid_files)} valid files.")

    def display_quote(self):
        self.write(get_random_quote())

    def display_articles(self):
        self.write(" Top Python Articles:")
        for article in scrape_articles():
            self.write(f" - {article}")

    def read_files(self):
        self.write(" Files in directory:")
        for file in os.listdir('.'):
            self.write(f" - {file}")
        try:
            with open("sample.txt", "r") as f:
                self.write(" Contents of sample.txt:")
                for line in f:
                    self.write(line.strip())
        except FileNotFoundError:
            self.write(" sample.txt not found.")

    def run_examples(self):
        # List comprehension
        nums = [1, 2, 3, 4, 5]
        evens = [n for n in nums if n % 2 == 0]
        self.write(f"Even numbers: {evens}")

        # Dict lookup
        user_ages = {"Alice": 30, "Bob": 25}
        self.write(f"Alice is {user_ages.get('Alice', 'unknown')} years old.")

        # Regex
        text = "An awesome apple always attracts attention."
        matches = re.findall(r"\ba\w*", text, re.IGNORECASE)
        self.write(f"Regex match: {matches}")

        # Class + Method
        class Dog:
            def __init__(self, name, breed):
                self.name = name
                self.breed = breed
            def bark(self): return f"{self.name} the {self.breed} says Woof!"

        d = Dog("Rex", "Labrador")
        self.write(d.bark())

        # Division error handling
        try:
            result = 10 / 0
        except ZeroDivisionError:
            self.write("Caught division by zero error.")

# -------------------------------
# SECTION 4: Main
# -------------------------------
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
