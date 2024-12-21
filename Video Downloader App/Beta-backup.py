from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import os
from moviepy.editor import *

def download():
    video_path = url_entry.get()
    file_path = destination_entry.get()
    
    try:
        print('Downloading...')
        yt = YouTube(video_path, on_progress_callback=progress_function)
        mp4 = yt.streams.get_highest_resolution().download(output_path=file_path)
        print('Download complete')
    except Exception as e:
        print('Error:', e)

def get_path():
    path = filedialog.askdirectory()
    destination_entry.delete(0, END)
    destination_entry.insert(0, path)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percentage
    window.update()

# creates the window using Tk() function
window = Tk()
# creates title for the window
window.title('MP4 Downloader')
# dimensions and position of the window
window.geometry('500x300+430+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)
# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=300)
canvas.pack()

# creating a ttk label for URL
url_label = ttk.Label(window, text='Enter video URL:')
# adding the label to the canvas
canvas.create_window(200, 50, window=url_label)
# creating a ttk entry for URL
url_entry = ttk.Entry(window, width=40)
# adding the entry to the canvas
canvas.create_window(200, 80, window=url_entry)

# creating a ttk label for destination folder
destination_label = ttk.Label(window, text='Select destination folder:')
# adding the label to the canvas
canvas.create_window(200, 120, window=destination_label)
# creating a ttk entry for destination folder
destination_entry = ttk.Entry(window, width=40)
# adding the entry to the canvas
canvas.create_window(200, 150, window=destination_entry)
# creating a button to select destination folder
destination_button = ttk.Button(window, text='Select', command=get_path)
# adding the button to the canvas
canvas.create_window(370, 150, window=destination_button)

# creating a button to download
download_button = ttk.Button(window, text='Download', command=download)
# adding the button to the canvas
canvas.create_window(200, 220, window=download_button)

# creating a progress bar
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=400, mode='determinate')
# adding the progress bar to the canvas
canvas.create_window(250, 270, window=progress_bar)

window.mainloop()
