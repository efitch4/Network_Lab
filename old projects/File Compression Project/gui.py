import tkinter as tk
from compressmodule import compress,decompress
from tkinter import filedialog


def open_file():
    filename = filedialog.askopenfilename(initialdir ='/',title="Select a file to comptress")
    return filename

def compression(i,o):
    compress(i,o)



window = tk.Tk()
window.title("Compression engine")
window.geometry("600x400")



input_entry = tk.Entry(window)
output_entry = tk.Entry(window)




compress_button = tk.Button(window,text="Compress",command=lambda:compression(open_file(),"compressedoutput1.txt"))


compress_button.grid(row=2,column=1)



window.mainloop()