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

def cov_crawling():
    
    driver.get('http://ncov.mohw.go.kr/')

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    return soup

class Covid_crawler:
    def __init__(self):
        pass
    
    def crawling(self, arg):
        
        if arg == "일일확진자":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(1)')

            rglrExprs = re.compile('일일 확진자|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed
    
        if arg == "일일완치자":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > ul > li:nth-child(2)')

            rglrExprs = re.compile('일일 완치자|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[1]} {cov_list[3]}명", color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "확진자":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(1)')

            rglrExprs = re.compile('확진환자|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "완치":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(2)')

            rglrExprs = re.compile('완치|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[0]} (격리해제) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 +{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed

        if arg == "치료중":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(3)')

            rglrExprs = re.compile('치료 중|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[0]} (격리 중) {cov_list[1]},{cov_list[2]}명", description=f'전일대비 -{cov_list[3]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed
    
        if arg == "사망":

            cov_source = cov_crawling().select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div > ul > li:nth-child(4)')

            rglrExprs = re.compile('사망|[0-9]+')

            cov_list = rglrExprs.findall(str(cov_source))

            embed = discord.Embed(title=f"{cov_list[0]} {cov_list[1]}명", description=f'전일대비 +{cov_list[2]}명', color=0xFF0000)
        
            embed.set_footer(text=f'{dt.month}.{dt.day}. 00시 기준')

            return embed
