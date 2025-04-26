import tkinter as tk
from tkinter import ttk, messagebox


def generate_sql():
    table = table_var.get()
    columns = column_entry.get()
    condition = condition_entry.get()

    if not table:
        messagebox.showerror("Error", "Table name is required!")
        return

    columns_part = columns if columns else "*"
    where_part = f" WHERE {condition}" if condition else ""
    sql_query = f"SELECT {columns_part} FROM {table}{where_part};"
    
    query_display.delete("1.0", tk.END)
    query_display.insert(tk.END, sql_query)


# Main application window
root = tk.Tk()
root.title("SQL Query Generator")
root.geometry("500x400")

# Table selection
tk.Label(root, text="Table Name:").pack(pady=5)
table_var = tk.StringVar()
table_entry = ttk.Entry(root, textvariable=table_var)
table_entry.pack(fill=tk.X, padx=10)

# Column selection
tk.Label(root, text="Columns (comma-separated, leave empty for *):").pack(pady=5)
column_entry = ttk.Entry(root)
column_entry.pack(fill=tk.X, padx=10)

# Condition input
tk.Label(root, text="Condition (e.g., id > 5):").pack(pady=5)
condition_entry = ttk.Entry(root)
condition_entry.pack(fill=tk.X, padx=10)

# Generate button
generate_button = ttk.Button(root, text="Generate SQL", command=generate_sql)
generate_button.pack(pady=10)

# SQL Query Display
tk.Label(root, text="Generated SQL Query:").pack(pady=5)
query_display = tk.Text(root, height=10, wrap=tk.WORD)
query_display.pack(fill=tk.BOTH, padx=10, pady=5)

# Run the application
root.mainloop()
