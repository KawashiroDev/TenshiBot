#TenshiBot Booru module V2
#Credits: EcchiBot by KaitoKid - The booru code is based on booru code from that bot however it has been modified to work with Tenshi
#https://github.com/KaitoKid/EcchiBot

#booru URL, used for safebooru command
booru = 'gelbooru.com'

#NSFW booru URL, used for gelbooru command
booru_nsfw = 'gelbooru.com'

#safebooru rating
#options are: safe, questionable, explicit
boorurating = 'safe'

#NSFW tag blacklist
#loli and shota are against Discord TOS
#Could also blacklist things like guro and futa but i don't want to become too restrictive with the booru stuff
boorublacklist_nsfw = '-loli+-lolicon+-shota+-shotacon'

badtags_moderate = '-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-bdsm+-lovestruck+-artificial_vagina+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-breast_hold+-nude+-butt_crack+-naked_apron+-cock+-yaoi+-penis+-shota+-loli+-sex+-femdom+-thighs+-smelling+-nazi+-swastika+-naked_cloak+-undressing+-naked_sheet+-groin+-drugs+-weed+-topless+-have_to_pee+-naked_towel+-no_panties+-naked_shirt+-shirt_lift+-erect_nipples+-gag+-gagged+-ball_gag+-downblouse+-you_gonna_get_raped+-convenient_leg+-convenient_arm+-underwear+-convenient_censoring+-bra+-trapped+-restrained+-skirt_lift+'


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

    #@commands.Cog.listener()
    #async def on_message(self, message):
        #print(message)
        #lang_jp = discord.utils.get(message.guild.roles, name="tenko_jp")
        #print (message.guild.me.roles)
        #lang_fr = discord.utils.get(message.guild.roles, name="tenko_fr")
        #if lang_jp in message.guild.me.roles:
            #print ("jp")
            #noposts_safe = '投稿は見つかりませんでした'
            #noposts_gel = '投稿は見つかりませんでした'
            #unavailable_safe = 'Safebooru is unavailable at this time'
            #unavailable_gel = 'Gelbooru is unavailable at this time'
            #embedtitle = "Booru画像"
            #sourcetitle = "画像ソース"
            #res_string = "画像の解像度"
            #query_string = "クエリ"
            #nosource_string = "ソースがリストされていません"
            #disabled = "disabledstring_jp"
            #nsfwchan = "nsfwstring_jp"

        #else:

            #noposts_safe = '**No posts found, Try:**\nChecking the tags are spelt correctly\nChanging your search query\nSearching with the Gelbooru command'
            #noposts_gel = '**No posts found, Try:**\nChecking the tags are spelt correctly\nChanging your search query'
            #unavailable_safe = 'Safebooru is unavailable at this time'
            #unavailable_gel = 'Gelbooru is unavailable at this time'
            #embedtitle = "Booru image"
            #sourcetitle = "Image source"
            #res_string = "Dimensions"
            #query_string = "Query"
            #nosource_string = "No source listed"
            #disabled = "This command cannot be used in this server"
            #nsfwchan = "This command can only be used in NSFW channels"


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def safebooru(self, ctx, *, tags):
        if int(ctx.guild.id) == int("486699197131915264"):
            await ctx.send('Error: command cannot be used in TPL')
            return
        else:
        
            async with aiohttp.ClientSession() as session:
                #async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tags) as r:
                async with session.get('http://' + 'gelbooru.com' + '/index.php?page=dapi&s=post&q=index&tags=rating:safe+-animated+-audio+-webm+' + badtags_moderate + tags) as r:
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
                            msg = "**No posts found, Try:**\nChecking the tags are spelt correctly\nChanging your search query\nSearching with the Gelbooru command"
                            await ctx.send(msg)
                            return

                        else:
                            source = ((soup.find('post'))('source'))
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            img_url = pic('file_url')
                            url_strip_start = str(img_url).strip('[<file_url>')
                            raw_url = str(url_strip_start).strip('</file_url>]')
                            img_id = pic('id')
                            id_strip_start = str(img_id).strip('[<id>')
                            sbooru_id = str(id_strip_start).strip('</id>]')

                            #sbooru_tags = pic['tags']
                            img_sauce = pic('source')
                            if img_sauce == '':
                                img_sauce = '[<source>No source listed</source>]'
                            source_strip_start = str(img_sauce).strip('[<source>')
                            sbooru_sauce = str(source_strip_start).strip('</source>]')
                            
                            img_width = pic('width')
                    
                            width_strip_start = str(img_width).strip('[<width>')
                            width = str(width_strip_start).strip('</width>]')

                            img_height = pic('height')
                            height_strip_start = str(img_height).strip('[<height>')
                            height = str(height_strip_start).strip('</height>]')
                            
                            #creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + str(raw_url))
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Sbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=width + "x" + height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_image(url=booruappend + msg)
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
                            source = ((soup.find('post'))('source'))
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            img_url = pic('file_url')
                            url_strip_start = str(img_url).strip('[<file_url>')
                            raw_url = str(url_strip_start).strip('</file_url>]')
                            img_id = pic('id')
                            id_strip_start = str(img_id).strip('[<id>')
                            sbooru_id = str(id_strip_start).strip('</id>]')

                            #sbooru_tags = pic['tags']
                            img_sauce = pic('source')
                            if img_sauce == '':
                                img_sauce = '[<source>No source listed</source>]'
                            source_strip_start = str(img_sauce).strip('[<source>')
                            sbooru_sauce = str(source_strip_start).strip('</source>]')
                            
                            img_width = pic('width')
                    
                            width_strip_start = str(img_width).strip('[<width>')
                            width = str(width_strip_start).strip('</width>]')

                            img_height = pic('height')
                            height_strip_start = str(img_height).strip('[<height>')
                            height = str(height_strip_start).strip('</height>]')
                            
                            #creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + str(raw_url))
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Sbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=width + "x" + height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_image(url=booruappend + msg)
                            await ctx.send(embed=em)

                            
                    msg = 'Gelbooru is unavailable at this time'
                    await ctx.send(msg)
                    return
        else:
            await ctx.send('Error: This command can only be used in NSFW channels')
            return

    @commands.slash_command(name="safebooru", description="Search Safebooru")
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def safebooru_slash(self, ctx, *, tags: str):
        if int(ctx.guild.id) == int("486699197131915264"):
            await ctx.send('Error: command cannot be used in TPL')
            return
        else:
        
            async with aiohttp.ClientSession() as session:
                #async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tags) as r:
                async with session.get('http://' + 'gelbooru.com' + '/index.php?page=dapi&s=post&q=index&tags=rating:safe+-animated+-audio+-webm+' + badtags_moderate + tags) as r:
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
                            msg = "**No posts found, Try:**\nChecking the tags are spelt correctly\nChanging your search query\nSearching with the Gelbooru command"
                            await ctx.send(msg)
                            return

                        else:
                            source = ((soup.find('post'))('source'))
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            img_url = pic('file_url')
                            url_strip_start = str(img_url).strip('[<file_url>')
                            raw_url = str(url_strip_start).strip('</file_url>]')
                            img_id = pic('id')
                            id_strip_start = str(img_id).strip('[<id>')
                            sbooru_id = str(id_strip_start).strip('</id>]')

                            #sbooru_tags = pic['tags']
                            img_sauce = pic('source')
                            if img_sauce == '':
                                img_sauce = '[<source>No source listed</source>]'
                            source_strip_start = str(img_sauce).strip('[<source>')
                            sbooru_sauce = str(source_strip_start).strip('</source>]')
                            
                            img_width = pic('width')
                    
                            width_strip_start = str(img_width).strip('[<width>')
                            width = str(width_strip_start).strip('</width>]')

                            img_height = pic('height')
                            height_strip_start = str(img_height).strip('[<height>')
                            height = str(height_strip_start).strip('</height>]')
                            
                            #creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + str(raw_url))
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Sbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=width + "x" + height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_image(url=booruappend + msg)
                            await ctx.send(embed=em)

                    msg = 'Gelbooru is unavailable at this time'
                    await ctx.respond(msg)
                    return


#This command requires the channel to be marked as a NSFW channel to work, this should prevent people abusing it
    @commands.slash_command(name="gelbooru", description="Search Gelbooru (NSFW channels only)")
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def gelbooru_slash(self, ctx, *, tags: str):
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
                            await ctx.respond(msg)
                            return

                        else:
                            source = ((soup.find('post'))('source'))
                            if num < 100:
                                pic = p[random.randint(0,num-1)]
                            elif page == maxpage:
                                pic = p[random.randint(0,99)]
                            else:
                                pic = p[random.randint(0,99)]
                            img_url = pic('file_url')
                            url_strip_start = str(img_url).strip('[<file_url>')
                            raw_url = str(url_strip_start).strip('</file_url>]')
                            img_id = pic('id')
                            id_strip_start = str(img_id).strip('[<id>')
                            sbooru_id = str(id_strip_start).strip('</id>]')

                            #sbooru_tags = pic['tags']
                            img_sauce = pic('source')
                            if img_sauce == '':
                                img_sauce = '[<source>No source listed</source>]'
                            source_strip_start = str(img_sauce).strip('[<source>')
                            sbooru_sauce = str(source_strip_start).strip('</source>]')
                            
                            img_width = pic('width')
                    
                            width_strip_start = str(img_width).strip('[<width>')
                            width = str(width_strip_start).strip('</width>]')

                            img_height = pic('height')
                            height_strip_start = str(img_height).strip('[<height>')
                            height = str(height_strip_start).strip('</height>]')
                            
                            #creator = pic['creator_id']
                            if sbooru_sauce == '':
                                sbooru_sauce = 'No source listed'
                            em = discord.Embed(title='', description='', colour=0x42D4F4)
                            em.set_author(name='Booru image')
                            em.set_image(url=booruappend + str(raw_url))
                            em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                            em.add_field(name="Sbooru ID", value=sbooru_id, inline=True)
                            em.add_field(name="Dimensions", value=width + "x" + height, inline=True)
                            em.add_field(name="Query", value="`" + tags + "`", inline=False)
                            #em.set_image(url=booruappend + msg)
                            await ctx.respond(embed=em)

                            
                    msg = 'Gelbooru is unavailable at this time'
                    await ctx.respond(msg)
                    return
        else:
            await ctx.respond('This command can only be used in NSFW channels')
            return
					                    

def setup(bot):
    bot.add_cog(booruCog(bot))
