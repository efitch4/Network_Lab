from pymediainfo import MediaInfo
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from threading import Thread


def is_file_downloaded(file_path, check_duration=1, max_retries=5, min_size_mb=1):
    """Check if the file size is stable or sufficiently large."""
    retries = 0
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB

    if file_size_mb < min_size_mb:
        print(f"File is too small to be complete: {file_path} ({file_size_mb:.2f} MB)")
        return False

    while retries < max_retries:
        initial_size = os.path.getsize(file_path)
        time.sleep(check_duration)
        final_size = os.path.getsize(file_path)
        if initial_size == final_size:
            print(f"File size is stable: {file_path}")
            return True
        retries += 1

    last_modified = os.path.getmtime(file_path)
    if time.time() - last_modified > 60:  # 60 seconds since last modification
        print(f"File not recently modified, assuming complete: {file_path}")
        return True

    print(f"File is still changing: {file_path}")
    return False


def can_play_movie(file_path):
    """Check if a movie file can be played using MediaInfo."""
    try:
        media_info = MediaInfo.parse(file_path)
        if not media_info.tracks:
            print(f"No tracks found in file: {file_path}")
            return False

        # Check for video and audio tracks
        has_video = any(track.track_type == "Video" for track in media_info.tracks)
        has_audio = any(track.track_type == "Audio" for track in media_info.tracks)

        if has_video and has_audio:
            print(f"File is playable: {file_path}")
            return True
        else:
            print(f"File missing video or audio tracks: {file_path}")
            return False

    except Exception as e:
        print(f"Error validating file with MediaInfo: {file_path}\n{e}")
        return False


def scan_file(file_path, complete_listbox, incomplete_listbox, progress_var, total_files, log_textbox):
    """Scan a single file for completeness and playback status."""
    print(f"Scanning file: {file_path}")
    log_textbox.insert(tk.END, f"Scanning file: {file_path}\n")
    log_textbox.see(tk.END)

    if is_file_downloaded(file_path):
        playable = can_play_movie(file_path)
        if playable:
            log_textbox.insert(tk.END, f"✅ File is complete and playable: {file_path}\n")
            complete_listbox.insert(tk.END, f"✅ {os.path.basename(file_path)} is complete and playable!")
        else:
            log_textbox.insert(tk.END, f"❌ Playback issues detected: {file_path}\n")
            incomplete_listbox.insert(tk.END, f"❌ {os.path.basename(file_path)} has playback issues.")
    else:
        log_textbox.insert(tk.END, f"⌛ File is still downloading or changing: {file_path}\n")
        incomplete_listbox.insert(tk.END, f"⌛ {os.path.basename(file_path)} is still downloading.")

    progress_var.set(progress_var.get() + (100 / total_files))
    log_textbox.insert(tk.END, f"Progress: {progress_var.get():.2f}%\n")
    log_textbox.see(tk.END)


def scan_selected_folders(folder_list, complete_listbox, incomplete_listbox, progress_bar, progress_var, log_textbox):
    """Scan all selected folders in a separate thread."""
    def threaded_scan():
        log_textbox.insert(tk.END, "Starting scan...\n")
        log_textbox.see(tk.END)

        complete_listbox.delete(0, tk.END)
        incomplete_listbox.delete(0, tk.END)

        if not folder_list:
            log_textbox.insert(tk.END, "No folders selected! Please add folders and try again.\n")
            log_textbox.see(tk.END)
            messagebox.showerror("Error", "No folders selected!")
            return

        movie_extensions = (".mp4", ".mkv", ".avi", ".mov")
        files_to_scan = []

        for folder in folder_list:
            log_textbox.insert(tk.END, f"Scanning folder: {folder}\n")
            log_textbox.see(tk.END)
            for root, _, files in os.walk(folder):
                for file_name in files:
                    if file_name.lower().endswith(movie_extensions):
                        files_to_scan.append(os.path.join(root, file_name))

        total_files = len(files_to_scan)
        log_textbox.insert(tk.END, f"Total files to scan: {total_files}\n")
        log_textbox.see(tk.END)

        if total_files == 0:
            log_textbox.insert(tk.END, "No video files found in the selected folders.\n")
            log_textbox.see(tk.END)
            messagebox.showinfo("No Files Found", "No video files found in the selected folders.")
            return

        progress_var.set(0)
        progress_bar['maximum'] = 100

        for file_path in files_to_scan:
            scan_file(file_path, complete_listbox, incomplete_listbox, progress_var, total_files, log_textbox)

        log_textbox.insert(tk.END, "Scan complete!\n")
        log_textbox.see(tk.END)
        messagebox.showinfo("Scan Complete", "Folder scan completed!")

    Thread(target=threaded_scan).start()


def drop_files(event, folder_list, entry_field, log_textbox):
    """Handle dropped files/folders."""
    dropped_files = root.tk.splitlist(event.data)
    for file_path in dropped_files:
        if os.path.isdir(file_path):  # Only accept directories
            folder_list.append(file_path)
            log_textbox.insert(tk.END, f"Added folder: {file_path}\n")
            log_textbox.see(tk.END)
            entry_field.insert(tk.END, f"{file_path}\n")
        else:
            log_textbox.insert(tk.END, f"Rejected (not a directory): {file_path}\n")
            log_textbox.see(tk.END)
            messagebox.showwarning("Warning", f"{file_path} is not a directory!")


# GUI Setup
root = TkinterDnD.Tk()
root.title("Is It Done Yet?")
root.geometry("800x750")

frame = tk.Frame(root)
frame.pack(pady=10)

folder_list = []

folder_display = tk.Text(frame, width=60, height=10)
folder_display.pack(side=tk.LEFT, padx=5)
folder_display.drop_target_register(DND_FILES)
folder_display.dnd_bind('<<Drop>>', lambda event: drop_files(event, folder_list, folder_display, log_textbox))

log_frame = tk.Frame(root)
log_frame.pack(pady=10)

log_label = tk.Label(log_frame, text="Real-Time Log:")
log_label.pack()

log_textbox = tk.Text(log_frame, width=80, height=15, wrap=tk.WORD)
log_textbox.pack()

progress_frame = tk.Frame(root)
progress_frame.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, length=500)
progress_bar.pack()

scan_button = tk.Button(
    progress_frame, text="Scan Selected Folders",
    command=lambda: scan_selected_folders(folder_list, complete_listbox, incomplete_listbox, progress_bar, progress_var, log_textbox)
)
scan_button.pack(pady=10)

results_frame = tk.Frame(root)
results_frame.pack(pady=10)

complete_label = tk.Label(results_frame, text="Complete Files:")
complete_label.grid(row=0, column=0, padx=10, pady=5)

complete_listbox = tk.Listbox(results_frame, width=50, height=15)
complete_listbox.grid(row=1, column=0, padx=10, pady=5)

incomplete_label = tk.Label(results_frame, text="Incomplete Files:")
incomplete_label.grid(row=0, column=1, padx=10, pady=5)

incomplete_listbox = tk.Listbox(results_frame, width=50, height=15)
incomplete_listbox.grid(row=1, column=1, padx=10, pady=5)

root.mainloop()
