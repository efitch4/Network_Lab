import os
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Lock
import requests
import csv
from tkinter.filedialog import asksaveasfilename

# TeamViewer API Configuration
API_TOKEN = "25635920-7LotNqRQQs4R5EgAg8J9"  # Replace with your actual API token
TEAMVIEWER_API_URL = "https://webapi.teamviewer.com/api/v1/devices"

# Thread safety for shared resources
results_lock = Lock()

def fetch_teamviewer_devices():
    """Fetches devices from the TeamViewer API."""
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
    }
    try:
        response = requests.get(TEAMVIEWER_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get('devices', [])
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to fetch devices: {e}")
        return []

def ping_host(host, results, device_status=None):
    """Pings a single host and stores the result. Falls back to TeamViewer status."""
    # First, attempt a local ping
    response = os.system(f"ping -n 1 -w 1000 {host} >nul 2>&1")  # For Windows
    # Use `ping -c 1 -W 1` on Linux/Mac
    local_status = "Online" if response == 0 else "Offline"
    
    # If local ping fails, check TeamViewer status (if provided)
    if local_status == "Offline" and device_status:
        with results_lock:
            results[host] = f"TeamViewer Status: {device_status}"
    else:
        with results_lock:
            results[host] = local_status

def display_results(results):
    """Displays the results in a new pop-up window."""
    results_window = tk.Toplevel(root)
    results_window.title("Ping and API Results")
    results_window.geometry("600x500")

    results_text = tk.Text(results_window, wrap=tk.WORD, height=20)
    results_text.pack(fill=tk.BOTH, padx=10, pady=10)

    results_text.insert(tk.END, "Online Machines:\n")
    results_text.insert(tk.END, "-----------------\n")
    for host, status in results.items():
        if "Online" in status:
            results_text.insert(tk.END, f"{host}: {status}\n")

    results_text.insert(tk.END, "\nOffline Machines:\n")
    results_text.insert(tk.END, "------------------\n")
    for host, status in results.items():
        if "Offline" in status:
            results_text.insert(tk.END, f"{host}: {status}\n")

    results_text.config(state=tk.DISABLED)
    close_button = ttk.Button(results_window, text="Close", command=results_window.destroy)
    close_button.pack(pady=5)

def start_ping():
    """Starts the ping operation."""
    hosts = input_text.get("1.0", tk.END).strip().splitlines()
    if not hosts:
        messagebox.showerror("Error", "Please enter at least one host to ping.")
        return

    # Fetch TeamViewer devices and map their statuses
    devices = fetch_teamviewer_devices()
    teamviewer_status = {device.get('alias', 'Unknown'): device.get('status', 'Offline') for device in devices}

    start_button.config(state=tk.DISABLED)
    progress_bar["value"] = 0
    progress_bar["maximum"] = len(hosts)
    results = {}

    def run_ping():
        for i, host in enumerate(hosts, start=1):
            ip_address = host.split("(")[-1].strip(")") if "(" in host else host
            # Use TeamViewer status as fallback
            device_status = teamviewer_status.get(host, None)
            ping_host(ip_address, results, device_status)
            progress_bar["value"] = i
            progress_bar.update_idletasks()
        display_results(results)
        start_button.config(state=tk.NORMAL)

    thread = Thread(target=run_ping)
    thread.daemon = True
    thread.start()

def load_teamviewer_devices():
    """Loads TeamViewer devices and uses their online status directly."""
    devices = fetch_teamviewer_devices()
    if devices:
        input_text.delete("1.0", tk.END)
        results = {}

        for device in devices:
            alias = device.get('alias', 'Unknown')
            ip_address = device.get('last_ip', None)
            status = device.get('status', 'Offline')

            device_entry = f"{alias} ({ip_address if ip_address else 'No IP'})"
            results[device_entry] = status.capitalize()

        display_results(results)
        messagebox.showinfo("Success", "TeamViewer devices loaded successfully.")
    else:
        messagebox.showwarning("No Devices", "No devices found or unable to fetch devices.")

def export_device_list():
    """Exports the TeamViewer device list to a CSV file."""
    devices = fetch_teamviewer_devices()
    if devices:
        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Device List As"
        )
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Alias", "IP Address", "Status"])  # Header row
                for device in devices:
                    alias = device.get('alias', 'Unknown')
                    ip_address = device.get('last_ip', 'No IP Available')
                    status = device.get('status', 'Unknown')
                    writer.writerow([alias, ip_address, status])
            messagebox.showinfo("Export Successful", f"Device list exported to {file_path}")
    else:
        messagebox.showwarning("Export Failed", "No devices to export.")

# Set up the main application window
root = tk.Tk()
root.title("Mass Ping Tool with TeamViewer Integration")
root.geometry("600x500")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill=tk.X)

tk.Label(input_frame, text="Enter Computer Names or IPs (one per line):").pack(anchor=tk.W)
input_text = tk.Text(input_frame, height=10)
input_text.pack(fill=tk.X, padx=5, pady=5)

# Add a scrollbar to the input_text widget
scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=input_text.yview)
input_text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Progress bar
progress_frame = tk.Frame(root)
progress_frame.pack(pady=20, fill=tk.X)

tk.Label(progress_frame, text="Progress:").pack(anchor=tk.W)
progress_bar = ttk.Progressbar(progress_frame, length=400, mode="determinate")
progress_bar.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Ping", command=start_ping)
start_button.pack(side=tk.LEFT, padx=5)

load_button = ttk.Button(button_frame, text="Load TeamViewer Devices", command=load_teamviewer_devices)
load_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(button_frame, text="Export Devices", command=export_device_list)
export_button.pack(side=tk.LEFT, padx=5)

exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()
