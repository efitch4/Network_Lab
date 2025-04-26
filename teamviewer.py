import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import threading
import requests

class TeamViewerMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TeamViewer Network Monitor")
        self.computer_list = []
        self.api_key = "25474929-oOjcXIpiOyiRSAXkYcpp"
        self.api_url = "https://webapi.teamviewer.com/api/v1/devices/"

        # GUI Elements
        self.file_label = tk.Label(root, text="Import CSV or enter computer names:")
        self.file_label.pack()

        self.import_button = tk.Button(root, text="Import CSV", command=self.import_csv)
        self.import_button.pack()

        self.text_box = tk.Text(root, height=10, width=50)
        self.text_box.pack()

        self.scan_button = tk.Button(root, text="Run Scan", command=self.run_scan)
        self.scan_button.pack()

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                self.computer_list = [row[0] for row in reader]
            messagebox.showinfo("Success", f"Imported {len(self.computer_list)} computers from CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV: {e}")

    def run_scan(self):
        self.computer_list += self.text_box.get("1.0", tk.END).strip().splitlines()
        self.computer_list = list(filter(None, self.computer_list))  # Remove empty lines

        if not self.computer_list:
            messagebox.showwarning("Warning", "No computers to scan.")
            return

        threading.Thread(target=self.scan_computers, daemon=True).start()

    def scan_computers(self):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(self.api_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed ot fetch data: {response.status_code} {response.text}")

            devices = response.json().get("devices", [])
            if not devices:
                raise Exception("No devices found inthe API response.")
            
            # Debug: Print API response to idenfity field issues
            print("Available devices:",[d.get("alias")for d in devices])

            results = []
            for computer_name in self.computer_list:
                print(f"Checking for:{computer_name}")

                device = next(
                   (d for d in devices if d.get("alias", "").lower() ==computer_name.lower()),
                   None 
                )
                if device:
                    # Safely handle 'onlineState'
                    status = device.get("onlineState","Unknown")
                    if status == "online":
                        results.append(f"{computer_name}: Online")
                    elif status == "offline":
                        results.append(f"{computer_name}: Offline")
                    else:
                        results.append(f"{computer_name}: Status Unknown")
                else:
                    results.append(f"{computer_name}: Not Found")
    #Show results in a popup
            self.show_results(results)

        except Exception as e:
            messagebox.showerror("Error", f"Error during scan: {e}")
    
    def show_results(self, results):
        if hasattr(self, "results_window") and self.results_window.winfo_exists():
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.root)
        self.results_window.title("Scan Results")

        self.results_window.protocol("WM_DELETE_WINDOW", self.clear_results)

        results_text = tk.Text(self.results_window, wrap=tk.WORD, height=20, width=50)
        results_text.pack()
        results_text.insert(tk.END, "\n".join(results))
        results_text.config(state=tk.DISABLED)

    def clear_results(self):
    # Clear any stored results when the window is closed
        if hasattr(self, "results_window") and self.results_window.winfo_exists():
            self.results_window.destroy()
        self.results_window = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TeamViewerMonitorApp(root)
    root.mainloop()
