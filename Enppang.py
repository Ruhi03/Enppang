# -*- coding:utf-8 -*-
import os
import sys
import discord
import asyncio
import json
import argparse

from School_menu import School_menu
from Covid_crawling import Covid_crawler
from Youtube_download import Youtube_downloader
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from os import system
from discord import Member
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

with open('Keys/Discord_token.txt', 'r') as token_key: # 토큰은 디스코드에서 받으세요
    token = token_key.readlines()[0]

with open('Keys/Youtube_api_key.txt', 'r') as api_Key: # API 키는 구글에서 받으세요
    DEVELOPER_KEY = api_Key.readlines()[0]

YOUTUBE_API_SERVICE_NAME = 'youtube'

YOUTUBE_API_VERSION = 'v3'

bot = commands.Bot(command_prefix='[[')

videos_title = []

videos_rink = []

nowplaying = ''

def music_number(number):
    
    musicnumber = Youtube_downloader()
    musicnumber.download(f'https://www.youtube.com/watch?v={videos_rink[number]}')
    
    global nowplaying
    
    nowplaying = videos_title[number]
    videos_rink.clear()

@bot.event
async def on_ready():
    
    print("{0} S T A R T {0}".format("*"*10))
    
    while True:
        
        await bot.change_presence(status=discord.Status.online,
        activity=discord.Game("멜빵 안입어"))
        await asyncio.sleep(10)
        
        await bot.change_presence(status=discord.Status.online,
        activity=discord.Game("-멜-"))
        await asyncio.sleep(10)
        
        await bot.change_presence(status=discord.Status.online,
        activity=discord.Game("멜빵 입고싶어"))
        await asyncio.sleep(1)
        
        await bot.change_presence(status=discord.Status.online,
        activity=discord.Game("은칠"))
        await asyncio.sleep(10)
        
        await bot.change_presence(status=discord.Status.online,
        activity=discord.Game("Silver Bread"))
        await asyncio.sleep(10)

@bot.command()
async def 명령어(ctx): # 전체 명령어
    
    embed = discord.Embed(title='명령어 목록', description='명령어 앞에 [[를 붙히면되요!!\n(기능 계속 추가중ㅜ)', color=0x929292)
    embed.add_field(name='음악', value='신청, 현재곡 ', inline=False)
    embed.add_field(name='코로나', value='확진자, 치료중, 완치, 사망, 일일 확진자, 일일완치자', inline=False)
    await ctx.send(embed=embed)

@bot.command() # 인사
async def 안녕(ctx):
    
    await ctx.send("안녕!")

@bot.command() # 멜빵
async def 멜빵(ctx):

    await ctx.send('야!!!!')

@bot.command(pass_context=True) # 사용자가 들어가있는 통화방으로 들어감
async def 들어와(ctx):
    
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(pass_context=True) # 통화방 나감
async def 나가(ctx):
    
    await ctx.voice_client.disconnect()

@bot.command()
async def 급식(ctx, arg): # 급식메뉴 기능 현재 보류중
    
    await ctx.send('아직 공사중,,')

@bot.command()
async def 코로나(ctx, arg):

    covid = Covid_crawler()
    embed = covid.crawling(arg)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 신청(ctx, *, search_data): # 노래 신청
    
    def youtube_search(options):
        
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(
        q=f'{search_data}',
        part='id,snippet',
        maxResults=10
        ).execute()

        videos_title.clear()

        for search_result in search_response.get('items', []):
            
            if search_result['id']['kind'] == 'youtube#video':
                
                videos_title.append('%s' % (search_result['snippet']['title']))
                videos_rink.append('%s' % (search_result['id']['videoId']))

    if __name__ == '__main__':
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default='Google')
        parser.add_argument('--max-results', help='Max results', default=25)
        args = parser.parse_args()

        try:
            
            youtube_search(args)
        
        except HttpError as e:
            
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    
    await ctx.send(f'''1.{videos_title[0]}
    2.{videos_title[1]}
    3.{videos_title[2]}
    4.{videos_title[3]}
    5.{videos_title[4]}''')

@bot.command(pass_context=True)
async def _1(ctx):
    
    music_number(0)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Music_downloads/song.mp3"))

@bot.command(pass_context=True)
async def _2(ctx):
    
    music_number(1)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Music_downloads/song.mp3"))

@bot.command(pass_context=True)
async def _3(ctx):
    
    music_number(2)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Music_downloads/song.mp3"))

@bot.command(pass_context=True)
async def _4(ctx):
    
    music_number(3)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Music_downloads/song.mp3"))

@bot.command(pass_context=True)
async def _5(ctx):
    
    music_number(4)
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Music_downloads/song.mp3"))

@bot.command(pass_context=True)
async def 현재곡(ctx):
    
    embed = discord.Embed(title=f'{nowplaying}', color=0x929292)
    await ctx.send(embed=embed)

bot.run(token)