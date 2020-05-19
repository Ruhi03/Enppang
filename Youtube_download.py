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
        print('노래 다운로드중!! 곧 재생됩니다!!')

class Youtube_downloader:

    def __init__(self):
        pass
    
    def download(self, rink):

        ydl_opts = {
        'outtmpl': 'Music_download/song.mp3',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        }
        
        if os.path.isfile('Music_download/song.mp3'):
            os.remove('Music_download/song.mp3')

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={rink}'])
