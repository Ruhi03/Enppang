import os
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'outtmpl': 'Music_downloads/song.mp3',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

class Youtube_downloader:
    def __init__(self):
        pass
    def download(self, url):
        song_there = os.path.isfile("Music_downloads/song.mp3")
        try:
            if song_there:
                os.remove("Music_downloads/song.mp3")
        except PermissionError:
            print("Wait for the current playing music end or use the 'stop' command")
            return
        print("Getting everything ready, playing audio soon")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])