import re
import nacl.utils
import requests
import urllib
import bs4
import datetime
import discord

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = True

driver = webdriver.Chrome('Crawling/chromedriver.exe', options=options)

dt = datetime.datetime.now()

def crawling_source(rink):
    
    driver.get(rink)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    return soup

class Covid_crawler:
    def __init__(self):
        pass
    
    def crawling(self, arg):

        rink = 'http://ncov.mohw.go.kr/'

        if arg == "일일확진자":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(1)')

            regex = re.compile('일일 확진자|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed
    
        if arg == "일일완치자":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(2)')

            regex = re.compile('일일 완치자|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "확진자":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(1)')

            regex = re.compile('확진환자|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "완치":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(2)')

            regex = re.compile('완치|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[0]} (격리해제) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "치료중":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(3)')

            regex = re.compile('치료 중|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[0]} (격리 중) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 -{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed
    
        if arg == "사망":

            covid_source = crawling_source(rink).select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(4)')

            regex = re.compile('사망|[0-9]+')

            cov_list = regex.findall(str(covid_source))

            embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]}명", description=f'전일대비 +{cov_list[2]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

class Weather_crawler:

    def __init__(self):
        pass

    def crawling(self, arg):
        
        
        rink = f'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={arg}날씨'

        weather_source = crawling_source(rink).select('#main_pack > div.sc.cs_weather._weather > div:nth-child(2) > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info > div > p > span.todaytemp')
        weather_source_2 = crawling_source(rink).select('#main_pack > div.sc.cs_weather._weather > div:nth-child(2) > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info > div > ul > li:nth-child(1) > p')
        regex = re.compile('[0-9]+')
        regex_2 = re.compile('비|흐림|맑음') # 나중에 확인하고 더 추가할 예정

        weather_list = regex.findall(str(weather_source))
        weather_list_2 = regex_2.findall(str(weather_source_2))

        if weather_list_2[0] == '비':
            weather_status = ':cloud_rain: '

        if weather_list_2[0] == '흐림':
            weather_status = ':cloud: '

        if weather_list_2[0] == '맑음':

            if 6 < dt.hour < 18:
                weather_status = ':sunny: '

            else:
                weather_status = ':crescent_moon: '

        embed = discord.Embed(title=f"{weather_status} 현재 {arg} 기온 {weather_list[0]}도", description='', color=0x99ffff)

        return embed