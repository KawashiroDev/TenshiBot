#TenshiBot Booru module
#Credits: EcchiBot by KaitoKid - The booru code is based on booru code from that bot however it has been modified to work with Tenshi
#https://github.com/KaitoKid/EcchiBot

#booru URL, used for safebooru command
booru = 'safebooru.org'

#NSFW booru URL, used for gelbooru command
booru_nsfw = 'gelbooru.com'

#safebooru rating
#options are: safe, questionable, explicit
boorurating = 'safe'

#NSFW tag blacklist
#loli and shota are against Discord TOS
#Could also blacklist things like guro and futa but i don't want to become too restrictive with the booru stuff
boorublacklist_nsfw = '-loli+-lolicon+-shota+-shotacon'

#appends text to the start of booru url output, gelbooru doesn't use this
booruappend = ''

import discord
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands
from bs4 import BeautifulSoup


class booruCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


		
#The traditional way of getting the message content works, args throw up an error if i try and use them here however the traditional way breaks with more than 1 prefix, i've countered this by using an if statement to check what the message starts this and use the correct strip based on what prefix is used, yes i know this is ghetto af but it works	
    @commands.command()
    async def safebooru(self, ctx, message):
        if ctx.message.content.startswith('='):
            tag = ctx.message.content[len("= safebooru"):].strip()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tag) as r:
                    if r.status == 200:
                        soup = BeautifulSoup(await r.text(), "lxml")
                        num = int(soup.find('posts')['count'])
                        maxpage = int(round(num/100))
                        page = random.randint(0, maxpage)
                        t = soup.find('posts')
                        p = t.find_all('post')
                        if num == 0: 
                            msg = 'No posts found, are the tags spelt correctly?'
                            await ctx.send(msg)
                            return

                        else:
                            source = ((soup.find('post'))['source'])
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,num%100 - 1)]
                            else:
                                pic = p[random.randint(0,99)]
                            msg = pic['file_url']
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + msg)
                            await ctx.send(embed=em)
        else:
            tag = ctx.message.content[len("<@571094749537239042> safebooru"):].strip()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tag) as r:
                    if r.status == 200:
                        soup = BeautifulSoup(await r.text(), "lxml")
                        num = int(soup.find('posts')['count'])
                        maxpage = int(round(num/100))
                        page = random.randint(0, maxpage)
                        t = soup.find('posts')
                        p = t.find_all('post')
                        if num == 0: 
                            msg = 'No posts found, are the tags spelt correctly?'
                            await ctx.send(msg)
                            return

                        else:
                            source = ((soup.find('post'))['source'])
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,num%100 - 1)]
                            else:
                                pic = p[random.randint(0,99)]
                            msg = pic['file_url']
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + msg)
                            await ctx.send(embed=em)

				
#This command requires the channel to be marked as a NSFW channel to work, this should prevent people abusing it
    @commands.command()
    async def gelbooru(self, ctx, message):
        if ctx.channel.is_nsfw():
            if ctx.message.content.startswith('='):
                tag = ctx.message.content[len("= gelbooru"):].strip()
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://' + booru_nsfw + '/index.php?page=dapi&s=post&q=index&tags=+' + boorublacklist_nsfw + '+'  + tag) as r:
                        if r.status == 200:
                            soup = BeautifulSoup(await r.text(), "lxml")
                            num = int(soup.find('posts')['count'])
                            maxpage = int(round(num/100))
                            page = random.randint(0, maxpage)
                            t = soup.find('posts')
                            p = t.find_all('post')
                            if num == 0: 
                                msg = 'No posts found, are the tags spelt correctly?'
                                await ctx.send(msg)
                                return

                            else:
                                source = ((soup.find('post'))['source'])
                                if num < 100:
                                    pic = p[random.randint(0,num-1)]
                                elif page == maxpage:
                                    pic = p[random.randint(0,num%100 - 1)]
                                else:
                                    pic = p[random.randint(0,99)]
                                msg = pic['file_url']
                                em = discord.Embed(title='', description='', colour=0x42D4F4)
                                em.set_author(name='Booru image')
                                em.set_image(url=msg)
                                await ctx.send(embed=em)
            else:
                tag = ctx.message.content[len("<@571094749537239042> gelbooru"):].strip()
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://' + booru_nsfw + '/index.php?page=dapi&s=post&q=index&tags=+' + boorublacklist_nsfw + '+'  + tag) as r:
                        if r.status == 200:
                            soup = BeautifulSoup(await r.text(), "lxml")
                            num = int(soup.find('posts')['count'])
                            maxpage = int(round(num/100))
                            page = random.randint(0, maxpage)
                            t = soup.find('posts')
                            p = t.find_all('post')
                            if num == 0: 
                                msg = 'No posts found, are the tags spelt correctly?'
                                await ctx.send(msg)
                                return

                            else:
                                source = ((soup.find('post'))['source'])
                                if num < 100:
                                    pic = p[random.randint(0,num-1)]
                                elif page == maxpage:
                                    pic = p[random.randint(0,num%100 - 1)]
                                else:
                                    pic = p[random.randint(0,99)]
                                msg = pic['file_url']
                                em = discord.Embed(title='', description='', colour=0x42D4F4)
                                em.set_author(name='Booru image')
                                em.set_image(url=msg)
                                await ctx.send(embed=em)							
							
        else:
            await ctx.send('Error: This command can only be used in NSFW channels')		


					                    

def setup(bot):
    bot.add_cog(booruCog(bot))
