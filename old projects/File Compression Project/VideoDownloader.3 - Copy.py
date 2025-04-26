from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import shutil
import threading
import os
import os.path
def download_mp4():
    canvas.itemconfig(status_text, text="Downloading MP4....")

    video_path = url_entry.get()
    file_path = path_label.cget("text")

    print('Downloading MP4....')
    yt = YouTube(video_path)
    mp4 = yt.streams.get_highest_resolution().download()

    shutil.move(mp4, file_path)

    root.after(1000, lambda: canvas.itemconfig(status_text, text="Download Complete"))

def download_mp3():
    canvas.itemconfig(status_text, text="Downloading MP3....")

    video_path = url_entry.get()
    file_path = path_label.cget("text")

    print('Downloading MP3...')
    yt = YouTube(video_path)
    
    #Download only the audo stream in MP3 format
    audio_streams = yt.streams.filter(only_audio=True).first()
    # audio_file_path = os.path.join(file_path, f"{yt.title}.mp3")
    audio_streams.download(output_path=file_path)
    
   # Rename the dowloaded file to match the video title
    
    downloaded_file_path = os.path.join(file_path,audio_streams.default_filename)
    os.rename(downloaded_file_path, os.path.join(file_path,f"{yt.title}.mp3"))

    root.after(1000, lambda: canvas.itemconfig(status_text, text="Download Complete"))

 # Use the existing MP4 file to extract audio
    mp4_filename = f"{yt.title}.mp4"
    mp4_filepath = os.path.join(file_path, mp4_filename.replace('/','_'))
    if  os.path.exists(mp4_filepath):
        print("MP4 already exists. Skipping audio extraction.")
    else:
        video_clip = VideoFileClip(mp4_filepath)
        #extract audio from the exisiting MP4
        audio_file = video_clip.audio
        audio_file_path = os.path.join(file_path, f"{yt.title}.mp3")
        audio_file.write_audiofile(audio_file_path)
        audio_file.close()
  
    root.after(1000, lambda: canvas.itemconfig(status_text, text="Download Complete"))  


def get_path():
    path = filedialog.askdirectory()
    path_label.config(text=path)

root = Tk()
root.title('Video downloader')
canvas = Canvas(root, width=400, height=300)
canvas.pack()

app_label = Label(root, text="Video downloader", fg="blue", font=('Arial',20))
canvas.create_window(200, 20, window=app_label)

url_label = Label(root, text="Enter video URL")
url_entry = Entry(root)
canvas.create_window(200, 80, window=url_label)
canvas.create_window(200, 100, window=url_entry)

path_label = Label(root, text="Select path to download")
path_button = Button(root, text="Select", command=get_path)
canvas.create_window(200, 150, window=path_label)
canvas.create_window(200, 170, window=path_button)

download_mp4_button = Button(root, text='Download MP4', command=download_mp4)
canvas.create_window(100, 250, window=download_mp4_button)

download_mp3_button = Button(root, text='Download MP3', command=download_mp3)
canvas.create_window(300, 250, window=download_mp3_button)

status_text = canvas.create_text(200, 220, text="", fill="green")

root.mainloop()