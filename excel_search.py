import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd

class ExcelSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Search Tool")
        self.root.geometry("800x500")
        
        self.file_path = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select an Excel file and enter a search term")
        self.label.pack(pady=5)
        
        self.open_button = tk.Button(self.root, text="Open Excel File", command=self.load_excel)
        self.open_button.pack(pady=5)
        
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        
        self.search_button = tk.Button(self.root, text="Search", command=self.search_excel)
        self.search_button.pack(pady=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Sheet", "Row", "Column", "Value"), show="headings")
        self.tree.heading("Sheet", text="Sheet")
        self.tree.heading("Row", text="Row")
        self.tree.heading("Column", text="Column")
        self.tree.heading("Value", text="Value")
        
        self.tree.column("Sheet", width=100)
        self.tree.column("Row", width=50)
        self.tree.column("Column", width=50)
        self.tree.column("Value", width=300)
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def load_excel(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if self.file_path:
            messagebox.showinfo("Success", f"Loaded file: {self.file_path}")
    
    def search_excel(self):
        search_term = self.search_entry.get()
        if not self.file_path:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term.")
            return
        
        self.tree.delete(*self.tree.get_children())  # Clear previous results
        
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet in xls.sheet_names:
                df = pd.read_excel(self.file_path, sheet_name=sheet, dtype=str)  # Read sheet as string to avoid errors
                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        if pd.notna(value) and search_term.lower() in str(value).lower():
                            self.tree.insert("", "end", values=(sheet, row_idx + 1, col_idx + 1, value))
            
            if not self.tree.get_children():
                messagebox.showinfo("No Results", "No matches found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelSearchApp(root)
    root.mainloop()
