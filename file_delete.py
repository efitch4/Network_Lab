import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def find_locking_process(path):
    """Find and log the process locking the file or folder."""
    try:
        handle_command = f'handle "{path}"'
        result = subprocess.run(handle_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "PID" in line:
                    print(f"Locking Process: {line}")  # Log locking process
        else:
            messagebox.showerror("Error", f"Could not identify locking process: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to find locking process: {e}")

def terminate_process(pid):
    """Force terminate the identified process."""
    try:
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
        messagebox.showinfo("Success", f"Terminated process with PID: {pid}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to terminate process with PID {pid}: {e}")

def force_delete(path):
    """Forcefully delete file or folder by resetting permissions."""
    try:
        # Grant full access to the current user
        subprocess.run(["icacls", path, "/grant", "Everyone:F", "/T", "/C"], check=True)
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        messagebox.showinfo("Success", f"Forcefully deleted: {path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to force delete {path}: {e}")

def unlock_and_delete(path):
    """Unlock and delete a file or folder, even if the script is already running as admin."""
    try:
        # Attempt to delete the file or folder directly
        if os.path.isfile(path):
            os.remove(path)
            messagebox.showinfo("Success", f"Successfully deleted file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            messagebox.showinfo("Success", f"Successfully deleted folder: {path}")
    except PermissionError as e:
        try:
            # Use Handle to unlock the file or folder
            handle_command = f'handle -c "{path}"'
            result = subprocess.run(handle_command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)  # Log output for debugging
            # Retry deletion
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            messagebox.showinfo("Success", f"Successfully unlocked and deleted: {path}")
        except subprocess.CalledProcessError as unlock_error:
            # If unlocking fails, try forceful deletion
            force_delete(path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete {path}: {e}")

def delete_file():
    """Delete the selected file."""
    file_path = filedialog.askopenfilename(title="Select a file to delete")
    if file_path:
        unlock_and_delete(file_path)

def delete_folder():
    """Delete the selected folder."""
    folder_path = filedialog.askdirectory(title="Select a folder to delete")
    if folder_path:
        unlock_and_delete(folder_path)

def main():
    """Main function to create the GUI."""
    if not is_admin():
        messagebox.showerror("Error", "Please run the script as an administrator.")
        return

    # Create the main window
    root = tk.Tk()
    root.title("Stubborn File Deleter")
    root.geometry("400x500")

    # File and folder deletion buttons
    file_button = tk.Button(root, text="Delete File", command=delete_file, width=20, height=2)
    file_button.pack(pady=10)

    folder_button = tk.Button(root, text="Delete Folder", command=delete_folder, width=20, height=2)
    folder_button.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()