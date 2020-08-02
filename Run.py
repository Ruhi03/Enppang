# -*- coding:utf-8 -*-
import discord
import asyncio
import Youtube_download as music
from discord.ext import commands

with open('Keys/Discord_token.txt', 'r') as token_key:  # 토큰은 디스코드에서 받으세요
    token = token_key.readlines()[0]

YOUTUBE_API_SERVICE_NAME = 'youtube'; YOUTUBE_API_VERSION = 'v3'

bot = commands.Bot(command_prefix='[[') # 명령어 접두사

music_list = [[],[]]
'''music_list 는 [  [ 예약된 노래 제목 ], [ 예약된 노래 링크 ]  ]'''

def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def wrapper(context):
    def check_msg(message):
        return context.author == message.author and context.channel == message.channel
    return check_msg
    
@bot.event
async def on_ready():
    print("\n{0} 작동!!!!!!!!!!!!!!! {0}\n".format(" * " * 10))

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

@bot.command(pass_context=True)
async def 신청(ctx, *, search_arg):
    embed, search_result = music.search(search_arg)
    '''search_result 는 [  [ 검색한 노래 제목 ], [ 검색한 노래 링크 ]  ]'''
    await ctx.send("아래쪽에서 대기열에 넣을 음악을 골라주세요!!",embed=embed)

    while True:
        answer = await bot.wait_for('message', timeout=30, check=wrapper(ctx))
                #check=lambda message: not message.author.bot)  

        try: # 입력값이 1과 5사이의 정수인지 확인
            if 0 < int(answer.content) < 6:
                search_number = int(answer.content)
                break

        except ValueError: # 정수가 아닌 것을 입력 할 경우
            await ctx.send("잘못 입력 하셨습니다. 다시 입력 해주세요!!")
            continue

        except TimeoutError: # 대답 시간을 초과하면
            await ctx.send("시간이 초과되었어요 :cry:")
            break

    if music_list == [[],[]]: # 노래 리스트가 비어 있다면
        music.download(search_result[1][search_number-1])
        music_list[0].append(search_result[0][search_number-1])
        music_list[1].append(search_result[1][search_number-1])

        if is_connected(ctx): # 현재 통화채널에 접속해 있다면
            ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))

        else:
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio("song.mp3"))
    
    else:
        music_list[0].append(search_result[0][search_number-1])
        music_list[1].append(search_result[1][search_number-1])

@bot.command(pass_context=True)
async def 현재곡(ctx): # 현재 재생 중인 노래를 embed로 채팅 채널에 메시지를 보냄
    embed = discord.Embed(title=f"{music_list[0][0]}",
            url=f'https://www.youtube.com/watch?v={music_list[1][0]}')
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def 스킵(ctx): # 노래를 스킵하고 리스트에 있는 다음 노래를 재생함
    '''현재는 노래가 예약 돼 있어도 자동으로 넘어가지 않기 때문에 수동으로 스킵을 해야 함'''
    if not music_list: # 노래 리스트가 차 있으면
        del music_list[0][0]
        del music_list[0][1]
        music.download(music_list[1][0])

        if is_connected(ctx):
            ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))

        else:
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio("song.mp3"))

    else:
        await ctx.send('스킵할 노래가 없습니다!')

bot.run(token)