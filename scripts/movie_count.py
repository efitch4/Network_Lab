import tkinter as tk
from tkinter import filedialog, messagebox
import os

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        count = count_movies(directory)
        messagebox.showinfo("Movie Count", f"Found {count} movies in the directory.")

def count_movies(directory):
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith((".mp4", ".avi", ".mkv")):  # Add more extensions if needed
            count += 1
    return count

# Create the main window
window = tk.Tk()
window.title("Movie Counter")

# Create a button to browse for a directory
browse_button = tk.Button(window, text="Select Directory", command=browse_directory)
browse_button.pack(pady=20)

# Start the main event loop
window.mainloop()