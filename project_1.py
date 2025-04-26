import os
import sqlite3
import smtplib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from threading import Thread, Event
from email.mime.text import MIMEText
from pymediainfo import MediaInfo

class AdvancedFileScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Is it done yet?")
        self.root.geometry("1000x800")
        self.db_path = "scan_results.db"
        self.setup_database()
        self.paths_list = []
        self.pause_event = Event()
        self.pause_event.set()

        self.settings = {
            "min_size_mb": 50,
            "min_duration_ms": 1000,
            "file_extensions": [".mp4", ".mkv", ".avi", ".mov"],
        }

        self.setup_ui()

    def setup_database(self):
        """Initializes the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                status TEXT,
                message TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_to_database(self, file_path, status, message):
        """Logs the scan results to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scan_results (file_path, status, message) VALUES (?, ?, ?)", (file_path, status, message))
        conn.commit()
        conn.close()

    def send_email_summary(self, complete_count, incomplete_count):
        """Sends an email summary of the scan results."""
        sender_email = "your_email@example.com"
        recipient_email = "recipient_email@example.com"
        subject = "Scan Summary"
        body = f"""
        Scan Summary:
        ----------------
        Complete Files: {complete_count}
        Incomplete Files: {incomplete_count}
        ----------------
        Thank you for using Ultimate File Scanner!
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        try:
            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login(sender_email, "your_password")
                server.sendmail(sender_email, recipient_email, msg.as_string())
            messagebox.showinfo("Email Sent", "Summary email sent successfully!")
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email: {e}")

    def preview_file_metadata(self, file_path):
        """Displays metadata of the selected file."""
        try:
            media_info = MediaInfo.parse(file_path)
            metadata = "\n".join([f"{track.track_type}: {track.to_data()}" for track in media_info.tracks])
            messagebox.showinfo("File Metadata", metadata)
        except Exception as e:
            messagebox.showerror("Metadata Error", f"Failed to retrieve metadata: {e}")

    def setup_ui(self):
        self.setup_folder_display()
        self.setup_log_area()
        self.setup_progress_bar()
        self.setup_buttons()
        self.setup_results_listboxes()
        self.setup_dashboard_view()
        self.setup_context_menus()

    def setup_folder_display(self):
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10)

        self.folder_display = tk.Text(folder_frame, width=80, height=5)
        self.folder_display.pack(side=tk.LEFT, padx=10)
        self.folder_display.drop_target_register(DND_FILES)
        self.folder_display.dnd_bind("<<Drop>>", self.drop_handler)

        scroll = tk.Scrollbar(folder_frame, command=self.folder_display.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.folder_display.config(yscrollcommand=scroll.set)

    def setup_log_area(self):
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10)

        tk.Label(log_frame, text="Real-Time Log:").pack()
        self.log_textbox = tk.Text(log_frame, width=100, height=10, wrap=tk.WORD)
        self.log_textbox.pack()

    def setup_progress_bar(self):
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=500)
        self.progress_bar.pack()

    def setup_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Scan", command=self.start_scan).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Pause", command=self.pause_scan).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Resume", command=self.resume_scan).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Send Email Summary", command=self.send_email_prompt).grid(row=0, column=3, padx=10)
        tk.Button(button_frame, text="Dashboard", command=self.open_dashboard).grid(row=0, column=4, padx=10)

    def setup_results_listboxes(self):
        results_frame = tk.Frame(self.root)
        results_frame.pack(pady=10)

        tk.Label(results_frame, text="Complete Files:").grid(row=0, column=0)
        self.complete_listbox = tk.Listbox(results_frame, width=50, height=10)
        self.complete_listbox.grid(row=1, column=0, padx=10)

        tk.Label(results_frame, text="Incomplete Files:").grid(row=0, column=1)
        self.incomplete_listbox = tk.Listbox(results_frame, width=50, height=10)
        self.incomplete_listbox.grid(row=1, column=1, padx=10)

    def setup_dashboard_view(self):
        self.dashboard_window = None

    def open_dashboard(self):
        """Displays the dashboard window."""
        if self.dashboard_window:
            self.dashboard_window.lift()
            return

        self.dashboard_window = tk.Toplevel(self.root)
        self.dashboard_window.title("Dashboard")
        self.dashboard_window.geometry("600x400")
        self.dashboard_window.protocol("WM_DELETE_WINDOW", lambda: self.close_dashboard())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM scan_results GROUP BY status")
        stats = cursor.fetchall()
        conn.close()

        stats_text = "\n".join([f"{status}: {count}" for status, count in stats])
        tk.Label(self.dashboard_window, text="Scan Statistics", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.dashboard_window, text=stats_text, justify=tk.LEFT).pack(pady=10)

    def close_dashboard(self):
        self.dashboard_window.destroy()
        self.dashboard_window = None

    def send_email_prompt(self):
        """Prompt to send email summary."""
        complete_count = self.complete_listbox.size()
        incomplete_count = self.incomplete_listbox.size()
        self.send_email_summary(complete_count, incomplete_count)

    def log(self, message):
        """Logs a message to the log area."""
        self.log_textbox.insert(tk.END, f"{message}\n")
        self.log_textbox.see(tk.END)

    def drop_handler(self, event):
        """Handles file drop events."""
        dropped_items = self.root.tk.splitlist(event.data)
        for item in dropped_items:
            if os.path.exists(item):
                self.paths_list.append(item)
                self.folder_display.insert(tk.END, f"{item}\n")
                self.log(f"Added: {item}")
            else:
                self.log(f"Invalid path: {item}")
                messagebox.showwarning("Invalid Path", f"Invalid path: {item}")

    def validate_file(self, file_path):
        """Validates the file based on user settings."""
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb < self.settings["min_size_mb"]:
            return False, "File too small"

        try:
            media_info = MediaInfo.parse(file_path)
            video_tracks = [track for track in media_info.tracks if track.track_type == "Video"]
            audio_tracks = [track for track in media_info.tracks if track.track_type == "Audio"]

            if not video_tracks or not audio_tracks:
                return False, "Missing video or audio tracks"

            for track in video_tracks:
                if not track.duration or track.duration < self.settings["min_duration_ms"]:
                    return False, "Duration too short"

            return True, "File is valid"
        except Exception as e:
            return False, f"Error validating file: {e}"

    def start_scan(self):
        """Starts the scanning process in a thread."""
        Thread(target=self.scan_files).start()

    def pause_scan(self):
        """Pauses the scanning process."""
        self.pause_event.clear()
        self.log("Scanning paused.")

    def resume_scan(self):
        """Resumes the scanning process."""
        self.pause_event.set()
        self.log("Scanning resumed.")

    def scan_files(self):
        """Scans files for validation."""
        self.log("Starting scan...")
        files_to_scan = self.get_files_to_scan()

        total_files = len(files_to_scan)
        self.progress_var.set(0)

        for idx, file_path in enumerate(files_to_scan):
            self.pause_event.wait()

            is_valid, message = self.validate_file(file_path)
            if is_valid:
                self.complete_listbox.insert(tk.END, f"✅ {file_path}")
                self.log(f"✅ {file_path} - {message}")
            else:
                self.incomplete_listbox.insert(tk.END, f"❌ {file_path}")
                self.log(f"❌ {file_path} - {message}")

            self.log_to_database(file_path, "Complete" if is_valid else "Incomplete", message)
            self.progress_var.set((idx + 1) / total_files * 100)

        self.log("Scan complete!")
        messagebox.showinfo("Scan Complete", "Scanning completed!")

    def get_files_to_scan(self):
        """Returns a list of all files to scan."""
        files_to_scan = []
        for path in self.paths_list:
            if os.path.isfile(path):
                if path.lower().endswith(tuple(self.settings["file_extensions"])):
                    files_to_scan.append(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file_name in files:
                        if file_name.lower().endswith(tuple(self.settings["file_extensions"])):
                            files_to_scan.append(os.path.join(root, file_name))
        return files_to_scan

    def setup_context_menus(self):
        """Sets up context menus for additional functionality."""
        self.folder_menu = tk.Menu(self.root, tearoff=0)
        self.folder_menu.add_command(label="Clear All", command=self.clear_folder_display)

        # Bind right-click to show the context menu
        self.folder_display.bind("<Button-3>", self.show_folder_menu)

    def show_folder_menu(self, event):
        """Displays the folder display context menu."""
        try:
            self.folder_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.folder_menu.grab_release()

    def clear_folder_display(self):
        """Clears the folder display."""
        self.folder_display.delete("1.0", tk.END)
        self.paths_list.clear()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = AdvancedFileScanner(root)
    root.mainloop()