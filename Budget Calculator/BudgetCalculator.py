import tkinter as tk
import csv

expenses = []
expense_names = []
entry_expense_name = None
initial_amount = 0.0

def store_money():
    global initial_amount
    initial_amount += float(entry_money.get())
    update_current_amount()

def add_expense():
    global entry_expense_name
    expense_value = float(entry_expense.get())
    expenses.append(expense_value)
    expense_name = entry_expense_name.get() if entry_expense_name else ""
    expense_names.append(expense_name)
    entry_expense.delete(0, tk.END)
    if entry_expense_name:
        entry_expense_name.delete(0, tk.END)
    else:
        entry_expense_name = tk.Entry(root)
        entry_expense_name.grid(row=4, column=1, padx=10, pady=10)
        entry_expense_name.focus_set()
        entry_expense_name.bind('<Return>', lambda event: add_expense_name(entry_expense_name.get()))
    update_current_amount()

def add_expense_name(expense_name):
    print(f"Expense Name: {expense_name}")
    expense_names.append(expense_name)

def display_current():
    update_current_amount()
    expenses_str = "\n".join([f"{i+1}. {expense_name}: {expense}" for i, (expense_name, expense) in enumerate(zip(expense_names, expenses))])
    current_window = tk.Toplevel(root)
    current_window.title("Current Status")
    label_current = tk.Label(current_window, text=f"Current amount: {initial_amount}")
    label_current.pack(padx=10, pady=10)
    label_expenses = tk.Label(current_window, text="Expenses:")
    label_expenses.pack(padx=10, pady=5)
    label_expenses_list = tk.Label(current_window, text=expenses_str, justify=tk.LEFT)
    label_expenses_list.pack(padx=10, pady=5)

def clear_all():
    global initial_amount, expenses
    initial_amount = 0.0
    expenses = []
    entry_money.delete(0, tk.END)
    entry_expense.delete(0, tk.END)
    label_current_amount.config(text="")
    label_expenses.config(text="")

def update_current_amount():
    global initial_amount
    current_amount = initial_amount - sum(expenses)
    label_current_amount.config(text=f"Current amount: {current_amount}")

def backspace():
    if expenses:
        expenses.pop()
        update_current_amount()

def export_to_csv():
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Expense Name", "Amount"])
            for expense_name, expense in zip(expense_names, expenses):
                writer.writerow([expense_name, expense])

root = tk.Tk()
root.title("Expense Tracker")

button_backspace = tk.Button(root, text="Backspace", command=backspace)
button_backspace.grid(row=3, column=3, padx=10, pady=10)

button_clear = tk.Button(root, text="Clear All", command=clear_all)
button_clear.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

label_money = tk.Label(root, text="Enter initial amount of money:")
label_money.grid(row=0, column=0, padx=10, pady=10)

entry_money = tk.Entry(root)
entry_money.grid(row=0, column=1, padx=10, pady=10)

button_store = tk.Button(root, text="Store Money", command=store_money)
button_store.grid(row=0, column=2, padx=10, pady=10)

label_current_amount = tk.Label(root, text="")
label_current_amount.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

label_expense = tk.Label(root, text="Enter expense amount:")
label_expense.grid(row=2, column=0, padx=10, pady=10)

entry_expense = tk.Entry(root)
entry_expense.grid(row=2, column=1, padx=10, pady=10)
entry_expense.bind('<Return>', lambda event: add_expense())

label_expense_name = tk.Label(root, text="Enter expense name:")
label_expense_name.grid(row=4, column=0, padx=10, pady=10)

entry_expense_name = tk.Entry(root)
entry_expense_name.grid(row=4, column=1, padx=10, pady=10)
entry_expense_name.bind('<Return>', lambda event: add_expense_name(entry_expense_name.get()))

button_add_expense = tk.Button(root, text="Add Expense", command=add_expense)
button_add_expense.grid(row=4, column=2, padx=10, pady=10)

button_display_current = tk.Button(root, text="Display Current", command=display_current)
button_display_current.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

label_expenses = tk.Label(root, text="")
label_expenses.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

button_export_to_csv = tk.Button(root, text="Export to CSV", command=export_to_csv)
button_export_to_csv.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
