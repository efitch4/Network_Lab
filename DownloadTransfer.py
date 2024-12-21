import tkinter as tk
from tkinter import filedialog
import shutil
import os

def transfer_movies():
    source_folder = r"C:\Users\Eric\Downloads"
    destination_folder = r"\\DESKTOP-FOAHFCS\Transfer"  # Make sure this path is correct
    selected_format = format_var.get()

    files_transferred = 0  # Counter for the number of files transferred

    for filename in os.listdir(source_folder):
        if filename.endswith(selected_format):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            try:
                shutil.move(source_path, destination_path)
                files_transferred += 1
                print(f"Transferred {filename} successfully from {source_path} to {destination_path}.")
            except Exception as e:
                print(f"Error transferring {filename}: {e}")

    if files_transferred == 0:
        print(f"No files with the format {selected_format} found in the source folder.")

# GUI setup
root = tk.Tk()
root.title("Movie Transfer")

format_label = tk.Label(root, text="Select Format:")
format_label.grid(row=0, column=0)

formats = ["MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV", "WEBM", "MPEG-2"]
format_var = tk.StringVar(root)
format_var.set(formats[0])
format_dropdown = tk.OptionMenu(root, format_var, *formats)
format_dropdown.grid(row=0, column=1)

transfer_button = tk.Button(root, text="Transfer Movies", command=transfer_movies)
transfer_button.grid(row=1, column=0, columnspan=2)

root.mainloop()
