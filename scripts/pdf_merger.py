import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.files = []

        # Button to select PDFs
        self.select_button = tk.Button(root, text="Select PDFs", command=self.select_files)
        self.select_button.pack(pady=10)

        # Listbox to show selected files
        self.file_listbox = tk.Listbox(root, width=80)
        self.file_listbox.pack(pady=5)

        # Button to merge PDFs
        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

    def select_files(self):
        selected_files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf")]
        )
        if selected_files:
            self.files = selected_files
            self.file_listbox.delete(0, tk.END)
            for file in self.files:
                self.file_listbox.insert(tk.END, file)

    def merge_pdfs(self):
        if not self.files:
            messagebox.showwarning("Warning", "No PDF files selected!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Merged PDF As"
        )

        if save_path:
            try:
                merger = PdfMerger()
                for pdf in self.files:
                    merger.append(pdf)
                merger.write(save_path)
                merger.close()
                messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
