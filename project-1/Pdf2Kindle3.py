import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess 
import os 
from ebooklib import epub



def extract_text_from_epub(epub_path):
   book = epub.read_epub(epub_path)
   text = ''
   for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            text += item.get_body_content().decode('utf-8') 
   return text

def extract_text_from_mobi(mobi_path):
    pass

def convert_to_azw3(text, output_path):
    print("Converting to AZW3...")
    print("Text to be converted:", text)
        # Rest of the function4
    temp_txt_path = 'temp.txt'
    with open(temp_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)


    # Use Calibre's ebook-convert command tool to convert text to MOBI
        
    subprocess.run(['ebook-convert', temp_txt_path, output_path])

    # Remove temporary text file
    os.remove(temp_txt_path)




def select_file(file_type, file_entry):
    global epub_entry
    file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", f"*.{file_type}")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def convert_to_kindle_format():
    file_path = epub_entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a a file")
        return
    
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".epub":
        text = extract_text_from_epub(file_path)
    elif file_extension == ".mobi":
        text= extract_text_from_mobi(file_path)
    else:
        messagebox.showerror("Error", "Unsupported file format")
        return
    kindle_file_path = filedialog.asksaveasfilename(defaultextension=".azw3",filetypes=[("Kindle Files", f"*azw3")])
    if kindle_file_path:
        convert_to_azw3(text, kindle_file_path)
        messagebox.showinfo("Conversion Complete", "EPUB converted to Kindle format successfully.")

root = tk.Tk()
root.title("EPUB to Kindle Converter")


# Create GUI elements
tk.Label(root, text="Select EPUB Files:").pack()
epub_entry = tk.Entry(root, width=50)
epub_entry.pack()
tk.Button(root, text="Browse", command=lambda: select_file("EPUB",epub_entry)).pack()
tk.Button(root, text="Convert to Kindle Format", command=convert_to_kindle_format).pack()
root.mainloop()
