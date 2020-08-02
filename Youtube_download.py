import os
import argparse
import discord
import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with open('Keys/Youtube_api_key.txt', 'r') as api_Key:  # API 키는 구글에서 받으세요
    DEVELOPER_KEY = api_Key.readlines()[0]

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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

ydl_opts = {
    'outtmpl': 'song.mp3',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
        }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }

def search(arg):
    videos_search = [[],[]]
    
    def youtube_search(options):
            
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
        q=f'{arg}',
        part='id,snippet',
        maxResults=10
        ).execute()

        for search_result in search_response.get('items', []):

            if search_result['id']['kind'] == 'youtube#video':
                videos_search[0].append('%s' % (search_result['snippet']['title']))
                videos_search[1].append('%s' % (search_result['id']['videoId']))

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    
    embed = discord.Embed(title=" ",
    description=f"1.{videos_search[0][0]}\n2.{videos_search[0][1]}\n \
    3.{videos_search[0][2]}\n4.{videos_search[0][3]}\n5.{videos_search[0][4]}")
    
    return embed, videos_search

def download(rink):

    if os.path.isfile('song.mp3'):
        os.remove('song.mp3')

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={rink}'])