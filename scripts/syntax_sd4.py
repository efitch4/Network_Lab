import os
import sqlite3
import threading
import requests
import json
from pathlib import Path
from tkinter import Tk, Button, Label, Text, filedialog, END
from tkinter import messagebox
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from unittest import mock, TestCase, main

# -------------------------------
# SECTION 1: Utility Functions
# -------------------------------

def get_all_files(directory, extensions):
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                matched_files.append(os.path.join(root, file))
    return matched_files

def safe_get_size_kb(file_path):
    try:
        return os.path.getsize(file_path) / 1024
    except Exception as e:
        print(f"Size error: {e}")
        return 0

# -------------------------------
# SECTION 2: Core Classes
# -------------------------------

class FileScanner:
    def __init__(self, min_size_kb=100):
        self.min_size_kb = min_size_kb
        self.valid_files = []

    def validate_file(self, file_path):
        size_kb = safe_get_size_kb(file_path)
        if size_kb >= self.min_size_kb:
            self.valid_files.append(file_path)
            return True
        return False

class MediaFileScanner(FileScanner):
    def __init__(self, min_size_kb=100, extensions=(".mp4", ".mkv", ".avi")):
        super().__init__(min_size_kb)
        self.extensions = extensions

    def scan_directory(self, folder):
        files = get_all_files(folder, self.extensions)
        for f in files:
            self.validate_file(f)
        return self.valid_files

class ScanLogger:
    def __init__(self, db_name="scan_results.db"):
        self.db_name = db_name
        self._setup_db()

    def _setup_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    status TEXT
                )
            """)

    def log(self, file_path, status):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO results (file_path, status) VALUES (?, ?)", (file_path, status))

# -------------------------------
# SECTION 3: API + Web Scraping
# -------------------------------

def get_random_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=5)
        data = res.json()
        return f'"{data["content"]}" - {data["author"]}'
    except Exception:
        return "Failed to fetch quote."

def scrape_python_articles():
    try:
        response = requests.get("https://realpython.github.io/fake-tasks/", timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="card-content")[:3]
        article_list = []
        for article in articles:
            title = article.find("h2", class_="title").text.strip()
            author = article.find("h3", class_="author").text.strip()
            article_list.append(f"{title} by {author}")
        return article_list
    except Exception:
        return ["Could not retrieve articles."]

# -------------------------------
# SECTION 4: Threaded Operation
# -------------------------------

def threaded_scan(scanner, folder, logger, output_callback):
    valid_files = scanner.scan_directory(folder)
    for file in valid_files:
        logger.log(file, "VALID")
    output_callback(f"✅ Scan complete: {len(valid_files)} valid files.")

# -------------------------------
# SECTION 5: GUI Application
# -------------------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Python Drill")
        self.textbox = Text(root, width=80, height=20)
        self.textbox.pack(pady=10)

        Button(root, text="Scan Folder", command=self.start_scan).pack()
        Button(root, text="Show Random Quote", command=self.show_quote).pack()
        Button(root, text="Scrape Python Articles", command=self.show_articles).pack()

        self.scanner = MediaFileScanner()
        self.logger = ScanLogger()

    def output(self, message):
        self.textbox.insert(END, f"{message}\n")
        self.textbox.see(END)

    def start_scan(self):
        folder = filedialog.askdirectory()
        if folder:
            thread = threading.Thread(target=threaded_scan, args=(self.scanner, folder, self.logger, self.output))
            thread.start()

    def show_quote(self):
        quote = get_random_quote()
        self.output(quote)

    def show_articles(self):
        articles = scrape_python_articles()
        self.output("Here are some helpful Python articles:")
        for article in articles:
            self.output(f" - {article}")

# -------------------------------
# SECTION 6: Unit Test Example
# -------------------------------

class TestScanner(TestCase):
    def test_validate_file_success(self):
        scanner = FileScanner(min_size_kb=0)
        with mock.patch("os.path.getsize", return_value=1024):
            result = scanner.validate_file("dummy.mp4")
            self.assertTrue(result)

    def test_validate_file_failure(self):
        scanner = FileScanner(min_size_kb=5000)
        with mock.patch("os.path.getsize", return_value=100):
            result = scanner.validate_file("small.mp4")
            self.assertFalse(result)

# Uncomment the line below to run tests
# if __name__ == "__main__": main()

# -------------------------------
# SECTION 7: Run the GUI
# -------------------------------

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

