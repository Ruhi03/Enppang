# -*- coding:utf-8 -*-
import os
import discord
import asyncio
import argparse

from School_menu import School_menu
from Crawlings import Covid_crawler
from Crawlings import Weather_crawler
from Youtube_download import Youtube_downloader
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord.ext import commands

with open('Keys/Discord_token.txt', 'r') as token_key:  # 토큰은 디스코드에서 받으세요
    token = token_key.readlines()[0]

with open('Keys/Youtube_api_key.txt', 'r') as api_Key:  # API 키는 구글에서 받으세요
    DEVELOPER_KEY = api_Key.readlines()[0]

YOUTUBE_API_SERVICE_NAME = 'youtube'; YOUTUBE_API_VERSION = 'v3'

bot = commands.Bot(command_prefix='[[')

search_title = []; search_rink = []; music_title = []

@bot.event
async def on_ready():
    print("{0} 작동!!!!!!!!!!!!!!! {0}".format(" * " * 10))

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
async def 명령어(ctx):  # 전체 명령어
    embed = discord.Embed(title='명령어 목록', description='명령어 앞에 [[를 붙히면되요!!\n(기능 계속 추가중ㅜ)', color=0x929292)
    embed.add_field(name='음악', value='신청, 현재곡 ', inline=False)
    embed.add_field(name='코로나', value='확진자, 치료중, 완치, 사망, 일일 확진자, 일일완치자', inline=False)
    embed.add_field(name='날씨', value='날씨 뒤에 지역명 붙여주시면되요!!', inline=False)
    await ctx.send(embed=embed)


@bot.command()  # 인사
async def 안녕(ctx):
    await ctx.send("안녕!")


@bot.command()  # 멜빵
async def 멜빵(ctx):
    await ctx.send('야!!!!')


@bot.command(pass_context=True)  # 사용자가 들어가있는 통화방으로 들어감
async def 들어와(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(pass_context=True)  # 통화방 나감
async def 나가(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def 급식(ctx, arg):  # 급식메뉴 기능 현재 보류중
    await ctx.send('아직 공사중,,')


@bot.command()
async def 코로나(ctx, arg):
    covid = Covid_crawler()
    embed = covid.crawling(arg)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 신청(ctx, *, search_data):
    
    def youtube_search(options):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)
        
        search_response = youtube.search().list(
            q=f'{search_data}',
            part='id,snippet',
            maxResults=10
        ).execute()

        for search_result in search_response.get('items', []):

            if search_result['id']['kind'] == 'youtube#video':
                search_title.append('%s' % (search_result['snippet']['title']))
                search_rink.append('%s' % (search_result['id']['videoId']))

    if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default='Google')
        parser.add_argument('--max-results', help='Max results', default=25)
        args = parser.parse_args()

        try:
            youtube_search(args)

        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    await ctx.send(f'''1.{search_title[0]}
2.{search_title[1]}
3.{search_title[2]}
4.{search_title[3]}
5.{search_title[4]}''')
    
    def wrapper(context):
        
        def check_msg(message):
            
            return context.author == message.author and context.channel == message.channel
        return check_msg
    
    answer = await bot.wait_for("message", timeout=180, check=wrapper(ctx))
    music_number = int(answer.content)
    
    for i in range(5):

        if music_number == i+1:
            music = Youtube_downloader()
            music_title.append(search_title[i])
            music.download(len(music_title), search_rink[i])

    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(f"Music_downloads/{len(music_title)} song.mp3"))

@bot.command(pass_context=True)
async def 현재곡(ctx):
    embed = discord.Embed(title=f'{music_title[0]}', color=0x929292)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 날씨(ctx, *, args):
    a = Weather_crawler()
    embed = a.crawling(args)
    await ctx.send(embed=embed)

bot.run(token)
