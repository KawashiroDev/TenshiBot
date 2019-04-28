#touhou image cog test

#these have to be defined in here too
#booru URL, used for touhou images and safebooru command
booru = 'safebooru.org'

#booru rating
#options are: safe, questionable, explicit
#affects the safebooru command only
boorurating = 'safe'

#booru tag blacklist
#results which have these tags won't be shown in the touhou commands
#does not affect the safebooru command
boorublacklist = '-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini'

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
booruappend = 'http:'

import discord
import requests
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands
from bs4 import BeautifulSoup


class ImageCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reimu(self, ctx):
        char = 'Hakurei_Reimu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(embed=em)  
					
					
    @commands.command()
    async def marisa(self, ctx):
        char = 'kirisame_marisa'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(embed=em)


    @commands.command()
    async def tenshi(self, ctx):
        char = 'hinanawi_tenshi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(embed=em)


    @commands.command()
    async def sakuya(self, ctx):
        char = 'izayoi_sakuya'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(embed=em)                    


                    

def setup(bot):
    bot.add_cog(ImageCog(bot))
