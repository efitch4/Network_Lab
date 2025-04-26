import os
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import requests
import csv

# TeamViewer API Configuration
API_TOKEN = "25473936-6rRwkLcXnfPVBAaycCJp"  # Replace with your actual API token
TEAMVIEWER_API_URL = "https://webapi.teamviewer.com/api/v1/devices"

def fetch_teamviewer_devices():
    """Fetches devices from the TeamViewer API."""
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
    }
    response = requests.get(TEAMVIEWER_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json().get('devices', [])
    else:
        messagebox.showerror("API Error", f"Failed to fetch devices: {response.text}")
        return []

def load_teamviewer_devices():
    """Loads filtered TeamViewer devices into the input text box."""
    devices = fetch_teamviewer_devices()
    if devices:
        input_text.delete("1.0", tk.END)
        online_devices = []
        offline_devices = []
        
        # Separate devices into online/offline categories
        for device in devices:
            alias = device.get('alias', 'Unknown')
            ip_address = device.get('last_ip', None)
            status = device.get('status', 'Offline')  # Default to Offline if not provided
            
            if ip_address:
                device_entry = f"{alias} ({ip_address})"
                if status.lower() == "online":
                    online_devices.append(device_entry)
                else:
                    offline_devices.append(device_entry)
        
        # Add online devices to the text box
        input_text.insert(tk.END, "Online Devices:\n")
        input_text.insert(tk.END, "----------------\n")
        for device in online_devices:
            input_text.insert(tk.END, f"{device}\n")

        # Add offline devices to the text box
        input_text.insert(tk.END, "\nOffline Devices:\n")
        input_text.insert(tk.END, "-----------------\n")
        for device in offline_devices:
            input_text.insert(tk.END, f"{device}\n")
        
        messagebox.showinfo("Success", "TeamViewer devices loaded successfully.")
    else:
        messagebox.showwarning("No Devices", "No devices found or unable to fetch devices.")

def export_device_list():
    """Exports the device list to a CSV file."""
    devices = fetch_teamviewer_devices()
    if devices:
        # Prepare device data for CSV export
        file_path = "teamviewer_devices.csv"
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

def ping_host(host, results):
    """Pings a single host and stores the result."""
    response = os.system(f"ping -n 1 -w 1000 {host} >nul 2>&1")  # For Windows
    # Use `ping -c 1 -W 1` on Linux/Mac
    if response == 0:
        results[host] = "Online"
    else:
        results[host] = "Offline"

def display_results(results):
    """Displays the results in a new pop-up window."""
    results_window = tk.Toplevel(root)
    results_window.title("Ping Results")
    results_window.geometry("400x300")

    results_text = tk.Text(results_window, wrap=tk.WORD, height=15)
    results_text.pack(fill=tk.BOTH, padx=10, pady=10)

    results_text.insert(tk.END, "Online Machines:\n")
    results_text.insert(tk.END, "-----------------\n")
    for host, status in results.items():
        if status == "Online":
            results_text.insert(tk.END, f"{host}\n")

    results_text.insert(tk.END, "\nOffline Machines:\n")
    results_text.insert(tk.END, "------------------\n")
    for host, status in results.items():
        if status == "Offline":
            results_text.insert(tk.END, f"{host}\n")

    results_text.config(state=tk.DISABLED)
    close_button = ttk.Button(results_window, text="Close", command=results_window.destroy)
    close_button.pack(pady=5)

def start_ping():
    """Starts the ping operation."""
    hosts = input_text.get("1.0", tk.END).strip().splitlines()
    if not hosts:
        messagebox.showerror("Error", "Please enter at least one host to ping.")
        return

    start_button.config(state=tk.DISABLED)
    progress_bar["value"] = 0
    progress_bar["maximum"] = len(hosts)
    results = {}

    def run_ping():
        for i, host in enumerate(hosts, start=1):
            # Extract IP address from the format "Alias (IP)"
            ip_address = host.split("(")[-1].strip(")") if "(" in host else host
            ping_host(ip_address, results)
            progress_bar["value"] = i
            progress_bar.update_idletasks()
        display_results(results)
        start_button.config(state=tk.NORMAL)

    thread = Thread(target=run_ping)
    thread.daemon = True
    thread.start()

# Set up the main application window
root = tk.Tk()
root.title("Mass Ping Tool with TeamViewer Integration")
root.geometry("500x400")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill=tk.X)

tk.Label(input_frame, text="Enter Computer Names or IPs (one per line):").pack(anchor=tk.W)
input_text = tk.Text(input_frame, height=10)
input_text.pack(fill=tk.X, padx=5, pady=5)

# Progress bar
progress_frame = tk.Frame(root)
progress_frame.pack(pady=20, fill=tk.X)

tk.Label(progress_frame, text="Progress:").pack(anchor=tk.W)
progress_bar = ttk.Progressbar(progress_frame, length=300, mode="determinate")
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
