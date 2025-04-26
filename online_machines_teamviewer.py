import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading
import http.client
import json

# Replace with your TeamViewer API token
API_TOKEN = "25474929-oOjcXIpiOyiRSAXkYcpp"
BASE_URL = "webapi.teamviewer.com"
ENDPOINT = "/api/v1/devices"


import http.client
import json
from tkinter import messagebox
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

BASE_URL = "api.example.com"
ENDPOINT = "/devices"
API_TOKEN = "your_api_token_here"

def fetch_device_status():
    """Fetch all devices from the TeamViewer API."""
    try:
        with http.client.HTTPSConnection(BASE_URL) as conn:
            headers = {
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json",
            }
            conn.request("GET", ENDPOINT, headers=headers)
            response = conn.getresponse()
            
            if response.status != 200:
                if response.status == 401:
                    messagebox.showerror("Error", "Unauthorized: Invalid API token.")
                elif response.status == 404:
                    messagebox.showerror("Error", "Endpoint not found.")
                else:
                    messagebox.showerror("Error", f"Unexpected status code: {response.status}")
                return []
            
            data = response.read()
            devices = json.loads(data)
            
            # Validate response structure
            if "devices" not in devices:
                messagebox.showerror("Error", "Malformed API response: 'devices' key not found.")
                return []
            
            # Debugging: Print all device IDs
            logging.debug(f"Device IDs from API: {[device.get('device_id') for device in devices.get('devices', [])]}")
            return devices.get("devices", [])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        return []



def check_devices():
    """Check the status of specific devices."""
    progress_var.set(0)
    online_list = []
    offline_list = []
    
    # Fetch the device list from the API
    device_data = fetch_device_status()
    if not device_data:
        return
    
    # Get the list of device IDs pasted into the text box
    input_text = input_box.get("1.0", tk.END).strip()
    device_ids_to_check = {id.strip().lower() for id in input_text.splitlines()}
    print("Device IDs from input box:", device_ids_to_check)  # Debugging
    
    # Filter API devices by the pasted device IDs
    devices = device_data.get("devices", [])
    total = len(device_ids_to_check)
    completed = 0
    
    for device in devices:
        device_id = device.get("device_id", "").strip().lower()
        if device_id in device_ids_to_check:
            name = device.get("alias", "Unknown Device")
            status = device.get("online_state", "unknown")
            if status == "online":
                online_list.append(name)
            else:
                offline_list.append(name)
            
            # Update progress bar
            completed += 1
            progress_var.set((completed / total) * 100)
            progress_label.config(text=f"{completed}/{total} completed ({progress_var.get():.0f}%)")
    
    # Update result boxes
    online_box.delete("1.0", tk.END)
    offline_box.delete("1.0", tk.END)
    online_box.insert(tk.END, "\n".join(online_list))
    offline_box.insert(tk.END, "\n".join(offline_list))
    
    if completed == 0:
        messagebox.showinfo("No Matches", "None of the pasted device IDs matched devices in the account.")
    else:
        messagebox.showinfo("Check Completed", "Device status check completed!")


def start_check_thread():
    threading.Thread(target=check_devices, daemon=True).start()


# GUI Setup
root = tk.Tk()
root.title("TeamViewer Device Status Checker")

# Input text area
input_label = tk.Label(root, text="Paste the list of device IDs here:")
input_label.pack(pady=5)
input_box = scrolledtext.ScrolledText(root, width=50, height=10)
input_box.pack(pady=5)

# Check button
check_button = tk.Button(root, text="Check Device Status", command=start_check_thread)
check_button.pack(pady=5)

# Progress bar and status
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=10, pady=5)
progress_label = tk.Label(root, text="0/0 completed (0%)")
progress_label.pack(pady=5)

# Results section
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

online_label = tk.Label(results_frame, text="Online Devices:")
online_label.grid(row=0, column=0, padx=10, pady=5)
online_box = scrolledtext.ScrolledText(results_frame, width=30, height=10, state='normal')
online_box.grid(row=1, column=0, padx=10, pady=5)

offline_label = tk.Label(results_frame, text="Offline Devices:")
offline_label.grid(row=0, column=1, padx=10, pady=5)
offline_box = scrolledtext.ScrolledText(results_frame, width=30, height=10, state='normal')
offline_box.grid(row=1, column=1, padx=10, pady=5)

# Run the main loop
root.mainloop()
