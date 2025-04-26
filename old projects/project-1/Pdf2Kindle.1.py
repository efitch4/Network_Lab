import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess 
import os 
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text 
    
def convert_to_mobi(text,output_path):
    temp_txt_path ='temp.txt'
    with open(temp_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    # Use Calibre's ebook-convert command tool to convert text to MOBI
        
    subprocess.run(['C:/Program Files/Calibre2/ebook-convert', temp_txt_path, output_path])

    # Remove temporary text file
    os.remove(temp_txt_path)

def select_pdf_file():
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, pdf_file_path)

def convert_to_kindle_format():
    pdf_path = pdf_entry.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file")
        return
    
    kindle_file_path = filedialog.asksaveasfilename(defaultextension=".mobi",filetypes=[("Kindle Files", "*.mobi")])
    if kindle_file_path:
        text = extract_text_from_pdf(pdf_path)
        convert_to_mobi(text, kindle_file_path)
        messagebox.showinfo("Conversion Complete", "PDF converted to Kindle format successfully.")

root = tk.Tk()
root.title("PDF to Kindle Converter")


# Create GUI elements
tk.Label(root, text="Select PDF Files:").pack()
pdf_entry = tk.Entry(root, width=50)
pdf_entry.pack()
tk.Button(root, text="Browse", command=select_pdf_file).pack()
tk.Button(root, text="Convert to Kindle Format", command=convert_to_kindle_format).pack()

root.mainloop()