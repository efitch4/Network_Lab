from pymediainfo import MediaInfo
import os 
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from threading import Thread

def validate_file(file_path, min_size_mb=50, min_duration_ms=1000):
    """Validates if a file is complete and playable."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb < min_size_mb:
        print(f"File to small: {file_path} ({file_size_mb:.2f} MB)")
        return False

    try:
        media_info = MediaInfo.parse(file_path)
        video_tracks = [track for track in media_info.tracks if track.track_type == "Video"]
        audio_tracks = [track for track in media_info.tracks if track.track_type == "Audio"]

        if not video_tracks or not audio_tracks:
            print(f"File missing video or audio tracks: {file_path}")
            return False

        for track in video_tracks:
            if not track.duration or track.duraction < min_duration_ms:
                print(f"Video track duration too short: {file_path}")
                return False

        print(f"File is valid and playable: {file_path}")
        return True

    except Exception as e:
        print(f"Error validating file: {file_path}\n{e}")
        return False
        