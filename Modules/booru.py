#TenshiBot Booru module V2
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

#unsafe tags
unsafetags = [
"underwear",
"sideboob",
"pov_feet",
"underboob",
"upskirt",
"sexually_suggestive",
"ass",
"bikini",
"bdsm",
"lovestruck",
]

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 5
#timeframe (seconds)
rlimit_time = 10
#

import discord
import aiohttp
#import praw
import lxml
import random
import asyncio

from discord.ext import commands
from bs4 import BeautifulSoup

wou = open("txt/warn_on_unsafe.txt", "r")
safeservers = wou.read()


class booruCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def safebooru(self, ctx, *, tags):
        if int(ctx.guild.id) == int("486699197131915264"):
            await ctx.send('Error: command cannot be used in TPL')
            return
        else:
        
            async with aiohttp.ClientSession() as session:
                #async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tags) as r:
                async with session.get('http://' + 'safebooru.org' + '/index.php?page=dapi&s=post&q=index&tags=rating:safe+-animated+-audio+-webm+' + tags) as r:
                    if r.status == 200:
                        soup = BeautifulSoup(await r.text(), "lxml")
                        num = int(soup.find('posts')['count'])
                        #print ('[Debug] num = ' + str(num))
                        maxpage = int(round(num/100))
                        #print ('[Debug] maxpage = ' + str(maxpage))
                        page = random.randint(0, maxpage)
                        #print ('[Debug] page = ' + str(page))
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
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            msg = pic['file_url']
                            sbooru_id = pic['id']
                            sbooru_tags = pic['tags']
                            sbooru_sauce = pic['source']
                            img_width = pic['width']
                            img_height = pic['height']
                            creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + msg)
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Sbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_image(url=booruappend + msg)
                            
                            if str(ctx.guild.id) in safeservers and any(c in sbooru_tags for c in unsafetags):
                                        unsafeimg = await ctx.send("This image may not be safe to view in public, React to view")
                                        await unsafeimg.add_reaction('\U0001f351')
                                        await asyncio.sleep(0.7)
                                        def check(reaction, user):
                                            return (str(reaction.emoji) == '\U0001f351')
                                       
                                        try:
                                            reaction, user = await self.bot.wait_for('reaction_add', timeout=30, check=check)
                                        except asyncio.TimeoutError:
                                            return
                                        else:
                                            if ((reaction.emoji) == '\U0001f351') and reaction.message.id == unsafeimg.id:
                                                em.set_footer(text="test")
                                                await ctx.send(embed=em)
                                                return
                            else:
                                await ctx.send(embed=em)
                                #print(tags)
                                #print (str(unsafetags))
                                #print (sbooru_tags)
                    
                    else:
                        msg = 'Safebooru is unavailable at this time'
                        await ctx.send(msg)
                        return

				
#This command requires the channel to be marked as a NSFW channel to work, this should prevent people abusing it
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def gelbooru(self, ctx, *, tags):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get('http://' + booru_nsfw + '/index.php?page=dapi&s=post&q=index&tags=+' + boorublacklist_nsfw + '+'  + tags) as r:
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
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            msg = pic['file_url']
                            sbooru_id = pic['id']
                            sbooru_tags = pic['tags']
                            sbooru_sauce = pic['source']
                            img_width = pic['width']
                            img_height = pic['height']
                            creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + msg)
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Gbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_footer(text="you may need to add rating:explict to your query if you were looking for nsfw images")
                            await ctx.send(embed=em)
                            return

                            
                    msg = 'Gelbooru is unavailable at this time'
                    await ctx.send(msg)
                    return
        else:
            await ctx.send('Error: This command can only be used in NSFW channels')
            return


					                    

def setup(bot):
    bot.add_cog(booruCog(bot))
