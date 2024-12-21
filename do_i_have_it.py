import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def sanitize_title(title):
    """Sanitize movie title by removing special characters, years, and converting to lowercase."""
    title = re.sub(r'\(\d{4}\)', '', title)  # Remove years in parentheses
    return re.sub(r'[^a-zA-Z0-9]', '', title).lower()  # Remove special characters and lowercase

def search_movies(directory, titles):
    """Search for movies in the directory."""
    found = {}
    not_found = []

    # Prepare sanitized titles for searching
    sanitized_titles = {title: sanitize_title(title) for title in titles}

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_sanitized = sanitize_title(file)
            for title, sanitized_title in sanitized_titles.items():
                if sanitized_title in file_sanitized:
                    found[title] = os.path.join(root, file)
    
    # Determine which titles were not found
    for title in titles:
        if title not in found:
            not_found.append(title)

    return found, not_found

def browse_directory():
    """Open a directory selection dialog."""
    directory = filedialog.askdirectory()
    entry_dir.delete(0, tk.END)
    entry_dir.insert(0, directory)

def search():
    """Perform the movie search based on user input."""
    directory = entry_dir.get().strip()
    titles_input = text_titles.get("1.0", tk.END).strip()
    titles = [line.strip() for line in titles_input.splitlines() if line.strip()]

    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    if not titles:
        messagebox.showerror("Error", "Please enter at least one movie title.")
        return

    found, not_found = search_movies(directory, titles)

    # Display results in the output box
    text_results.delete("1.0", tk.END)
    if found:
        text_results.insert(tk.END, "Found Movies:\n")
        for title, path in found.items():
            text_results.insert(tk.END, f"{title}: {path}\n")
        text_results.insert(tk.END, "\n")
    else:
        text_results.insert(tk.END, "No movies found.\n\n")

    if not_found:
        text_results.insert(tk.END, "Not Found Movies:\n")
        for title in not_found:
            text_results.insert(tk.END, f"{title}\n")

def clear_results():
    """Clear the search results."""
    text_results.delete("1.0", tk.END)

# Create the main application window
root = tk.Tk()
root.title("Bulk Movie Search")
root.geometry("600x600")

# Directory selection
frame_dir = tk.Frame(root)
frame_dir.pack(pady=10)
label_dir = tk.Label(frame_dir, text="Directory to search:")
label_dir.pack(side=tk.LEFT, padx=5)
entry_dir = tk.Entry(frame_dir, width=50)
entry_dir.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame_dir, text="Browse", command=browse_directory)
btn_browse.pack(side=tk.LEFT, padx=5)

# Movie titles input
label_titles = tk.Label(root, text="Enter movie titles (one per line):")
label_titles.pack(pady=5)
text_titles = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70)
text_titles.pack(pady=5)

# Search button
btn_search = tk.Button(root, text="Search", command=search)
btn_search.pack(pady=10)

# Results output
label_results = tk.Label(root, text="Search Results:")
label_results.pack(pady=5)
text_results = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
text_results.pack(pady=5)

# Clear button
btn_clear = tk.Button(root, text="Clear Results", command=clear_results)
btn_clear.pack(pady=10)

# Run the application
root.mainloop()
