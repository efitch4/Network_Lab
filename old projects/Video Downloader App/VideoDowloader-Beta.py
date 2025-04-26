from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import os
from moviepy.editor import *
import threading

def download():
    video_path = url_entry.get()
    file_path = destination_entry.get()
    
    try:
        print('Downloading...')
        yt = YouTube(video_path)
        yt.register_on_progress_callback(lambda stream, chunk, bytes_remaining: progress_function(stream, chunk, bytes_remaining))  # Register progress callback
        mp4 = yt.streams.get_highest_resolution().download(output_path=file_path)
        mp4_filename = os.path.basename(mp4)
        
        # Convert MP4 to MP3
        progress_label.config(text="Converting to MP3...")
        video_clip = VideoFileClip(mp4)
        audio_clip = video_clip.audio
        mp3_filename = os.path.splitext(mp4_filename)[0] + ".mp3"
        mp3_path = os.path.join(file_path, mp3_filename)
        t = threading.Thread(target=convert_to_mp3, args=(audio_clip, mp3_path))
        t.start()
        
    except Exception as e:
        progress_label.config(text=f"Error: {e}")
        print('Error:', e)

def convert_to_mp3(audio_clip, mp3_path):
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()
    progress_label.config(text="Download and conversion complete")
    progress_bar['value'] = 100  # Set progress bar to 100% when complete
    print('Download and conversion complete')

def get_path():
    path = filedialog.askdirectory()
    destination_entry.delete(0, END)
    destination_entry.insert(0, path)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Download progress: {percentage:.2f}%")  # Add this line to check progress
    progress_bar['value'] = percentage

    # Update the progress status label
    progress_label.config(text=f"Downloading: {percentage:.1f}%")
    
    window.update_idletasks()  # Update the GUI to reflect changes

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
canvas.create_window(230, 220, window=download_button)

# Creating a label to display progress status
progress_label = ttk.Label(window, text="")
canvas.create_window(250, 270, window=progress_label)  # Adjust the position as needed

# creating a progress bar
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=400, mode='determinate')
# adding the progress bar to the canvas
canvas.create_window(250, 250, window=progress_bar)

window.mainloop()
