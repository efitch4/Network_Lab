import socket
import tkinter as tk
from tkinter import messagebox

def scan_ports(target, start_port, end_port):
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    # Display results in a new window
    results_window = tk.Toplevel(root)
    results_window.title("Port Scan Results")
    results_label = tk.Label(results_window, text="Port Scan Results")
    results_label.pack()
    results_text = tk.Text(results_window)
    if open_ports:
        results_text.insert(tk.END, f"Open ports on {target}: {open_ports}")
    else:
        results_text.insert(tk.END, f"No open ports found on {target} in range {start_port}-{end_port}.")
    results_text.pack()

def open_port_scan_window():
    port_scan_window = tk.Toplevel(root)
    port_scan_window.title("Port Scanner")

    label_target = tk.Label(port_scan_window, text="Target:")
    label_target.grid(row=0, column=0, sticky="e")

    entry_target = tk.Entry(port_scan_window)
    entry_target.grid(row=0, column=1)

    label_ports = tk.Label(port_scan_window, text="Ports (e.g., 1-100):")
    label_ports.grid(row=1, column=0, sticky="e")

    entry_ports = tk.Entry(port_scan_window)
    entry_ports.grid(row=1, column=1)

    def run_port_scan():
        target = entry_target.get()
        port_range = entry_ports.get()

        if not target or not port_range:
            messagebox.showerror("Error", "Target or port range is empty")
            return

        try:
            # Parse start and end ports
            start_port, end_port = map(int, port_range.split('-'))
            scan_ports(target, start_port, end_port)
        except ValueError:
            messagebox.showerror("Error", "Invalid port range format. Use format 'start-end' (e.g., '1-100').")

    button_scan = tk.Button(port_scan_window, text="Scan Ports", command=run_port_scan)
    button_scan.grid(row=2, columnspan=2, pady=10)

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Networking Tools")

# Button to open port scanner window
button_port_scan = tk.Button(root, text="Port Scanner", command=open_port_scan_window)
button_port_scan.pack(pady=10)

root.mainloop()
