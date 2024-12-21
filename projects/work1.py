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


import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, messagebox

def process_bulk_xml():
    # Open file dialog to select multiple XML files
    Tk().withdraw()  # Hide the root Tkinter window
    file_paths = filedialog.askopenfilenames(title="Select XML Files", filetypes=[("XML Files", "*.xml")])
    
    if not file_paths:
        messagebox.showinfo("No Files", "No XML files were selected.")
        return

    for file_path in file_paths:
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate through all <Image_Name> tags
            for image_name in root.findall(".//Image_Name"):
                original_name = image_name.text
                if original_name and '0' in original_name:
                    # Replace the first '0' with '9'
                    new_name = original_name.replace('0', '9', 1)
                    image_name.text = new_name

            # Overwrite the original XML file without the XML declaration
            with open(file_path, "wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=False)

        except Exception as e:
            # Log error for a specific file and continue with the next
            messagebox.showerror("Error", f"Failed to process file: {file_path}\nError: {e}")
            continue

    messagebox.showinfo("Success", "All selected files were processed successfully.")

# Call the function
process_bulk_xml()

