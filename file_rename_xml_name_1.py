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

            # Overwrite the original XML file
            tree.write(file_path, encoding="utf-8", xml_declaration=True)

        except Exception as e:
            # Log error for a specific file and continue with the next
            messagebox.showerror("Error", f"Failed to process file: {file_path}\nError: {e}")
            continue

    messagebox.showinfo("Success", "All selected files were processed successfully.")

# Call the function
process_bulk_xml()
