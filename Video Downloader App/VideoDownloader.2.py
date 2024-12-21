from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *
import shutil
import threading


def download():
    #Display "Downloading ....."message
    canvas.itemconfig(status_text, text="Downloading....")

    video_path = url_entry.get()
    file_path = path_label.cget("text")

   #Download the video 
    print('Downloading....')
    yt = YouTube(video_path)
    mp4 = yt.streams.get_highest_resolution().download()
    video_clip = VideoFileClip(mp4)
    
    #code for mp3
    audio_file = video_clip.audio
    audio_file_path = f"{yt.title}.mp3"
    audio_file.write_audiofile(audio_file_path)
    audio_file.close()
    
    # Move audio file to destination
    shutil.move(audio_file_path, file_path)
    
    #Move video file to destination
    shutil.move(mp4, file_path)

    # Display "Download Complete " message after a delay
    root.after(1000, lambda: canvas.itemconfig(status_text, text="Download Complete"))

    canvas.itemconfig(status_text, text="Download Complete")    

def get_path():
    path = filedialog.askdirectory()
    path_label.config(text=path)

root =Tk()
root.title('Video downloader')
canvas = Canvas(root,width=400,height=300)
canvas.pack()

#app label 
app_label = Label(root,text="Video downloader",fg="blue",font=('Arial',20))
canvas.create_window(200,20,window=app_label)

#entry to accept video URL
url_label = Label(root,text="Enter video URL")
url_entry = Entry(root)
canvas.create_window(200,80,window=url_label)
canvas.create_window(200,100,window=url_entry)

#path to download videos
path_label = Label(root,text="Select path to download")
path_button = Button(root,text="Select",command=get_path)
canvas.create_window(200,150,window=path_label)
canvas.create_window(200,170,window=path_button)

#download button
download_button = Button(root,text='Download',command=download)
canvas.create_window(200,250,window=download_button)

#Status text on canvas
status_text = canvas.create_text(200, 220, text="", fill="green")

root.mainloop()