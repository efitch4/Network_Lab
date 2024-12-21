import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess 
import os 
from PyPDF2 import PdfReader
import epub
from ebooklib import epub

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() 
    return text 

def convert_to_mobi(text, output_path):
    temp_txt_path = 'temp.txt'
    with open(temp_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    # Use Calibre's ebook-convert command tool to convert text to MOBI
    subprocess.run(['C:/Program Files/Calibre2/ebook-convert', temp_txt_path, output_path])

    # Remove temporary text file
    os.remove(temp_txt_path)

def extract_text_from_epub(epub_path):
    try:
        book = epub.read_epub(epub_path)
        text = ''
        for item in book.get_items():
            if isinstance(item, epub.EpubHtml):
                text += item.get_body_content().decode('utf-8')
        return text
    except Exception as e:
        messagebox.showerror("Error", "Failed to extract text from EPUB")

def convert_to_azw3(text, output_path):
    if text is None:
        messagebox.showerror("Error", "No text to convert")
        return
    print("Converting to AZW3...")
    print("Text to be converted:", text)
    # Rest of the function4
    temp_txt_path = 'temp.txt'
    with open(temp_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    # Use Calibre's ebook-convert command tool to convert text to AZW3
    subprocess.run(['C:/Program Files/Calibre2/ebook-convert', temp_txt_path, output_path])

    # Remove temporary text file
    os.remove(temp_txt_path)

def select_pdf_file(entry):
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        entry.delete(0, tk.END)
        entry.insert(0, pdf_file_path)

def select_epub_file(entry):
    epub_file_path = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
    if epub_file_path:
        entry.delete(0, tk.END)
        entry.insert(0, epub_file_path)

def convert_pdf_to_kindle_format():
    pdf_path = pdf_entry.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return
    
    kindle_file_path = filedialog.asksaveasfilename(defaultextension=".mobi", filetypes=[("Kindle Files", "*.mobi")])
    if kindle_file_path:
        text = extract_text_from_pdf(pdf_path)
        convert_to_mobi(text, kindle_file_path)
        messagebox.showinfo("Conversion Complete", "PDF converted to Kindle format successfully.")

def convert_pdf_to_azw3_format():
    pdf_path = pdf_entry_azw3.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return
    
    azw3_file_path = filedialog.asksaveasfilename(defaultextension=".azw3", filetypes=[("Kindle Files", "*.azw3")])
    if azw3_file_path:
        text = extract_text_from_pdf(pdf_path)
        convert_to_azw3(text, azw3_file_path)
        messagebox.showinfo("Conversion Complete", "PDF converted to Kindle AZW3 format successfully.")

def convert_epub_to_kindle_format():
    epub_path = epub_entry.get()
    if not epub_path:
        messagebox.showerror("Error", "Please select an EPUB file")
        return
    
    kindle_file_path = filedialog.asksaveasfilename(defaultextension=".azw3", filetypes=[("Kindle Files", "*.azw3")])
    if kindle_file_path:
        text = extract_text_from_epub(epub_path)
        convert_to_azw3(text, kindle_file_path)
        messagebox.showinfo("Conversion Complete", "EPUB converted to Kindle format successfully.")

# Create the main window
root = tk.Tk()
root.title("File Converter")

# Create a canvas
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Add GUI elements for PDF to Kindle conversion
pdf_label = tk.Label(canvas, text="Convert PDF to Kindle Format")
pdf_label.pack()
pdf_entry = tk.Entry(canvas, width=50)
pdf_entry.pack()
pdf_button = tk.Button(canvas, text="Browse", command=lambda: select_pdf_file(pdf_entry))
pdf_button.pack()
pdf_to_kindle_button = tk.Button(canvas, text="Convert to Kindle Format", command=convert_pdf_to_kindle_format)
pdf_to_kindle_button.pack()

# Add GUI elements for PDF to Kindle AZW3 conversion
pdf_label_azw3 = tk.Label(canvas, text="Convert PDF to Kindle AZW3 Format")
pdf_label_azw3.pack()
pdf_entry_azw3 = tk.Entry(canvas, width=50)
pdf_entry_azw3.pack()
pdf_button_azw3 = tk.Button(canvas, text="Browse", command=lambda: select_pdf_file(pdf_entry_azw3))
pdf_button_azw3.pack()
pdf_to_kindle_button_azw3 = tk.Button(canvas, text="Convert to Kindle AZW3 Format", command=convert_pdf_to_azw3_format)
pdf_to_kindle_button_azw3.pack()

# Add GUI elements for EPUB to Kindle conversion
epub_label = tk.Label(canvas, text="Convert EPUB to Kindle Format")
epub_label.pack()
epub_entry = tk.Entry(canvas, width=50)
epub_entry.pack()
epub_button = tk.Button(canvas, text="Browse", command=lambda: select_epub_file(epub_entry))
epub_button.pack()
epub_to_kindle_button = tk.Button(canvas, text="Convert to Kindle Format", command=convert_epub_to_kindle_format)
epub_to_kindle_button.pack()

root.mainloop()