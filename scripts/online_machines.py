import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json


class TeamViewerChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("TeamViewer Machine Status")
        self.api_token = tk.StringVar()

        # API Token Input
        tk.Label(root, text="API Token:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.api_token, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Check Status", command=self.check_status).grid(row=0, column=2, padx=10, pady=10)

        # Results Table
        self.tree = ttk.Treeview(root, columns=("Machine", "Status"), show="headings")
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def check_status(self):
        """Fetch and display the status of machines from TeamViewer API."""
        token = self.api_token.get().strip()
        if not token:
            messagebox.showerror("Error", "API Token is required")
            return

        url = "https://webapi.teamviewer.com/api/v1/devices"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            # Build the request
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                data = response.read().decode()
                devices = json.loads(data).get("devices", [])

            # Clear existing data
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Populate the table with new data
            for device in devices:
                self.tree.insert(
                    "", "end", values=(device.get("alias"), "Online" if device.get("onlineState") == "online" else "Offline")
                )

        except urllib.error.URLError as e:
            messagebox.showerror("Error", f"API Error: {e}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse the API response")


if __name__ == "__main__":
    root = tk.Tk()
    app = TeamViewerChecker(root)
    root.mainloop()
