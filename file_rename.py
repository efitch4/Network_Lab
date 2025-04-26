import os
from tkinter import Tk, filedialog, Button, Label, messagebox

def process_files():
    # Open file dialog for selecting files
    file_paths = filedialog.askopenfilenames(title="Select Files")
    if not file_paths:
        messagebox.showinfo("No Files", "No files were selected.")
        return

    for file_path in file_paths:
        directory, filename = os.path.split(file_path)
        # Modify the filename
        if "_" in filename:
            base, ext = filename.split("_", 1)
            new_filename = "9" + base[1:] + ".pdf"
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            try:
                os.rename(file_path, new_file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {filename}: {e}")
                continue

    messagebox.showinfo("Success", "Files were renamed successfully.")

# Create the GUI
root = Tk()
root.title("Filename Modifier")

# Add a label and a button
Label(root, text="Select PDF files to modify:").pack(pady=10)
Button(root, text="Select Files", command=process_files).pack(pady=10)

# Run the GUI
root.mainloop()
