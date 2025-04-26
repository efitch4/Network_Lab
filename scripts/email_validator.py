import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import extract_msg
import os

class MsgToEmlConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MSG to EML Converter")
        self.root.geometry("650x450")

        # File Selection
        self.label = tk.Label(root, text="Select a .MSG file to convert:")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Browse .MSG File", command=self.load_msg_file)
        self.select_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to .EML", command=self.convert_to_eml)
        self.convert_button.pack(pady=5)

        # Output Box
        self.output = scrolledtext.ScrolledText(root, width=80, height=15)
        self.output.pack(pady=10)

        self.msg_path = None

    def load_msg_file(self):
        """Loads a .MSG file using file dialog"""
        self.msg_path = filedialog.askopenfilename(filetypes=[("Outlook MSG Files", "*.msg")])
        if self.msg_path:
            messagebox.showinfo("File Selected", f"Loaded: {self.msg_path}")
            self.output.insert(tk.END, f"Selected file: {self.msg_path}\n")

    def convert_to_eml(self):
        """Converts selected .MSG file to .EML, ensuring all headers (DKIM, SPF) are included"""
        if not self.msg_path:
            messagebox.showerror("Error", "No .MSG file selected.")
            return

        try:
            msg = extract_msg.Message(self.msg_path)
            msg_sender = msg.sender
            msg_to = msg.to
            msg_subject = msg.subject
            msg_date = msg.date
            msg_body = msg.body

            # Extract Full Raw Headers
            raw_headers = msg.headerDict  # Extracts full headers as a dictionary
            formatted_headers = "\n".join([f"{key}: {value}" for key, value in raw_headers.items()])

            # Check for DKIM signature
            if "DKIM-Signature" in raw_headers:
                self.output.insert(tk.END, "✅ DKIM Signature Found\n")
            else:
                self.output.insert(tk.END, "❌ No DKIM Signature Found\n")

            # Construct standard email headers for EML format
            email_headers = (
                f"From: {msg_sender}\n"
                f"To: {msg_to}\n"
                f"Subject: {msg_subject}\n"
                f"Date: {msg_date}\n"
                "Content-Type: text/plain; charset=UTF-8\n\n"
            )

            # Ask user where to save the .eml file
            eml_path = filedialog.asksaveasfilename(defaultextension=".eml",
                                                    filetypes=[("EML Files", "*.eml")],
                                                    initialfile=os.path.splitext(os.path.basename(self.msg_path))[0] + ".eml")

            if not eml_path:
                return  # User canceled save operation

            # Save .eml file
            with open(eml_path, "w", encoding="utf-8") as eml_file:
                eml_file.write(formatted_headers + "\n\n")  # Ensure all headers are saved
                eml_file.write(email_headers)
                eml_file.write(msg_body)

            self.output.insert(tk.END, f"✅ Conversion Successful: {eml_path}\n")
            messagebox.showinfo("Success", f"Converted to: {eml_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion Failed: {e}")
            self.output.insert(tk.END, f"❌ Conversion Error: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MsgToEmlConverter(root)
    root.mainloop()
