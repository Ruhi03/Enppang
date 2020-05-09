# -*- coding:utf-8 -*-
import os
import sys
import re
import discord
import asyncio
import nacl.utils
import requests
import json
import urllib
import bs4
import datetime
import youtube_dl
import argparse

from Youtube_download import Youtube_downloader
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from os import system
from urllib.request import urlopen
from discord import Member
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

with open('Keys/Discord_token.txt', 'r') as token_key:
    token = token_key.readlines()[0]

with open('Keys/Youtube_api_key.txt', 'r') as api_Key:
    DEVELOPER_KEY = api_Key.readlines()[0]

YOUTUBE_API_SERVICE_NAME = 'youtube'

YOUTUBE_API_VERSION = 'v3'

options = Options()

options.headless = True

driver = webdriver.Chrome('Crawling/chromedriver.exe', options=options)

dt = datetime.datetime.now()

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

def cov_crawling():
    
    driver.get('http://ncov.mohw.go.kr/')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    return soup

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
async def 명령어(ctx):
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
async def 급식(ctx, arg):

    if arg == "경민":
        
        await ctx.send("경민 급식 보여줄 예정")

    elif arg == "의공고":
        
        school_menu_url = "https://schoolmenukr.ml/api/high/J100000757?&hideAllergy=true"
        
        response = requests.get(school_menu_url)
        
        school_menu = json.loads(response.text)
        
        await ctx.send("{}".format(school_menu))

    else:
        
        await ctx.send("아직 추가되지않은 학교입니다")

@bot.command()
async def 코로나(ctx, *, args):

    if args == "일일확진자":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(1)')

        rglrExprs = re.compile('일일 확진자|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)
    
    elif args == "일일완치자":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(2)')

        rglrExprs = re.compile('일일 완치자|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)

    elif args == "확진자":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(1)')

        rglrExprs = re.compile('확진환자|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)

    elif args == "완치":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(2)')

        rglrExprs = re.compile('완치|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[0]} (격리해제) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)

    elif args == "치료중":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(3)')

        rglrExprs = re.compile('치료 중|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[0]} (격리 중) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 -{cov_list[3]}명', color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)
    
    elif args == "사망":

        cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(4)')

        rglrExprs = re.compile('사망|[0-9]+')

        cov_list = rglrExprs.findall(str(cov_source))

        embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]}명", description=f'전일대비 +{cov_list[2]}명', color=0xFF0000)
        
        embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 신청(ctx, *, search_date):
    
    def youtube_search(options):
        
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)
        
        search_response = youtube.search().list(
        q=f'{search_date}',
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