import os
from tkinter import Tk, filedialog, Button, Label, messagebox

def process_files():
    # Open file dialog for selecting multiple files
    Tk().withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("All Files", "*.*")])
    if not file_paths:
        messagebox.showinfo("No Files", "No files were selected.")
        return

    for file_path in file_paths:
        directory, filename = os.path.split(file_path)

        # Ensure the filename is modified properly
        name, extension = os.path.splitext(filename)  # Split name and extension
        
        if name:
            # Replace the first '0' in the filename with '9'
            modified_name = name.replace("0", "9", 1)
            
            # Keep only the part before '_index', then add '_index'
            if "_index" in modified_name:
                modified_name = modified_name.split("_index")[0] + "_index"

            # Combine the modified name with the original extension
            new_filename = f"{modified_name}{extension}"
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            try:
                os.rename(file_path, new_file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {filename}: {e}")
                continue

    messagebox.showinfo("Success", "All selected files were renamed successfully.")

# Create the GUI
root = Tk()
root.title("Filename Modifier")

# Add a label and a button
Label(root, text="Select files to modify:").pack(pady=10)
Button(root, text="Select Files", command=process_files).pack(pady=10)

# Run the GUI
root.mainloop()
