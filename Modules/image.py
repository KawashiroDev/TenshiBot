#TenshiBot Image module

#these have to be defined in here too
#booru URL, used for touhou images and safebooru command
booru = 'gelbooru.com'

#booru rating
#options are: safe, questionable, explicit
#affects the safebooru command only
boorurating = 'safe'

#booru tag blacklist
#results which have these tags won't be shown in the touhou commands
#does not affect the safebooru command
#huge filesize is blacklisted to help fix some images not embedding
boorublacklist = 'rating:safe+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-animated+-audio+-webm+rating:safe+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron'

boorublacklistgif = 'rating:safe+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-audio+-webm+rating:safe+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron'

#tag blacklist v2

#base tags to apply to all levels (except gifs)
boorutags_base = 'solo+rating:safe+-6%2Bgirls+-comic+-greyscale+-huge_filesize+-animated+-audio+-webm+-absurdres'
#artists whose works slip by the tag filters
badartists = '+-nori_tamago'
#base tags for gif command
boorutags_gif = 'rating:safe+-6%2Bgirls+-comic+-greyscale+-huge_filesize+-audio+-webm+-absurdres'
#default blacklisted tags (full SFW mode)
badtags_strict = '-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-bdsm+-lovestruck+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nude+-butt_crack+-naked_apron'
#tags to blacklist in moderate mode
badtags_moderate = '+-pov_feet+-bdsm+-lovestruck+-nude+-blood+-artificial_vagina+-sexually_suggestive+-upskirt+-penetration_gesture'
#tags to blacklist in an NSFW channel
badtags_nsfwmode = ''

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
#safebooru URL's used to need http added to the start but now they dont anymore
booruappend = ''

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 4
#timeframe (seconds)
rlimit_time = 11
#

import discord
import requests
import aiohttp
import praw
import lxml
import random
import asyncio
import twitter

from discord.ext import commands
from bs4 import BeautifulSoup


keiki_title = [
"Character image!",
"Create!",     
"oh!",
]

#twitter stuff
t_api = open("Tokens/twitter_consumer.txt", "r")
tw_api = t_api.read()
t_secret = open("Tokens/twitter_consumer_secret.txt", "r")
tw_secret = t_secret.read()
t_access = open("Tokens/twitter_access.txt", "r")
tw_access = t_access.read()
t_access_secret = open("Tokens/twitter_access_secret.txt", "r")
tw_access_secret = t_access_secret.read()



api = twitter.Api(consumer_key=tw_api,
consumer_secret=tw_secret,
access_token_key=tw_access,
access_token_secret=tw_access_secret)

class ImageCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def reimu(self, ctx):
        char = 'Hakurei_Reimu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xb50404)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)  
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def marisa(self, ctx):
        char = 'kirisame_marisa'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xf5e942)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def tenshi(self, ctx):
        char = 'hinanawi_tenshi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def tenshi_react(self, ctx):
        char = 'hinanawi_tenshi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



                        



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def tenshi2(self, ctx):
        char = 'hinanawi_tenshi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    msg2 = pic['change']
                    em = discord.Embed(title='', description='' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(msg)
                    await ctx.send('img_source:' + source)
                    await ctx.send(str(pic))
                    print(pic)
                    print(msg2)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def tenshi3(self, ctx):
        #define the character tag
        char = 'hinanawi_tenshi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image | Moderate mode'
            print("moderate role")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sakuya(self, ctx):
        char = 'izayoi_sakuya'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xc7c7c7)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)

                    
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def cirno(self, ctx):
        char = 'cirno'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x00e5ff)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def meiling(self, ctx):
        char = 'hong_meiling'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x04b548)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def flandre(self, ctx):
        char = 'flandre_scarlet'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xb50404)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def rumia(self, ctx):
        char = 'rumia'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xf5da42)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def rinnosuke(self, ctx):
        char = 'morichika_rinnosuke'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def murasa(self, ctx):
        char = 'murasa_minamitsu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
					

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mamizou(self, ctx):
        char = 'futatsuiwa_mamizou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
					




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def shou(self, ctx):
        char = 'toramaru_shou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def nemuno(self, ctx):
        char = 'sakata_nemuno'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def eternity(self, ctx):
        char = 'eternity_larva'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
					




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def narumi(self, ctx):
        char = 'yatadera_narumi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def daiyousei(self, ctx):
        char = 'daiyousei'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x04b548)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def ringo(self, ctx):
        char = 'ringo_(touhou)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xe2a81e)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kosuzu(self, ctx):
        char = 'motoori_kosuzu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def akyuu(self, ctx):
        char = 'hieda_no_akyuu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def hatate(self, ctx):
        char = 'himekaidou_hatate'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xb50480)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mima(self, ctx):
        char = 'mima'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sariel(self, ctx):
        char = 'sariel'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yumemi(self, ctx):
        char = 'okazaki_yumemi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def shinki(self, ctx):
        char = 'shinki'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                        



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def lily(self, ctx):
        char = 'lily_white'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def shion(self, ctx):
        char = 'yorigami_shion'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x048cb5)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def joon(self, ctx):
        char = "yorigami_jo'on"
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xaa4fa0)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def seiran(self, ctx):
        char = 'seiran_(touhou)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x6b87bd)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def koakuma(self, ctx):
        char = 'koakuma'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x990000)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def raiko(self, ctx):
        char = 'horikawa_raiko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xd25859)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def okina(self, ctx):
        char = 'matara_okina'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xe69454)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mai(self, ctx):
        char = 'teireida_mai'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x4e7764)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def satono(self, ctx):
        char = 'nishida_satono'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xe262b0)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def aunn(self, ctx):
        char = 'komano_aun'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def komachi(self, ctx):
        char = 'onozuka_komachi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xd25859)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def wakasagihime(self, ctx):
        char = 'wakasagihime'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def seija(self, ctx):
        char = 'kijin_seija'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xaeb4c6)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ')
                    em.set_image(url=booruappend + msg)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def toyohime(self, ctx):
        char = 'watatsuki_no_toyohime'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x583b80)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yorihime(self, ctx):
        char = 'watatsuki_no_yorihime'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xa84384)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def renko(self, ctx):
        char = 'usami_renko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def maribel(self, ctx):
        char = 'maribel_hearn'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def nue(self, ctx):
        char = 'houjuu_nue'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x000000)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def iku(self, ctx):
        char = 'nagae_iku'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def elly(self, ctx):
        char = 'elly'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kasen(self, ctx):
        char = 'ibaraki_kasen'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xfb959e)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def keine(self, ctx):
        char = 'kamishirasawa_keine'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x574b8c)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def konngara(self, ctx):
        char = 'konngara'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yuyuko(self, ctx):
        char = 'saigyouji_yuyuko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xff40d9)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def aya(self, ctx):
        char = 'shameimaru_aya'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xe58a53)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def nitori(self, ctx):
        char = 'kawashiro_nitori'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xb2daef)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sumireko(self, ctx):
        char = 'usami_sumireko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xaa6ad3)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def okuu(self, ctx):
        char = 'reiuji_utsuho'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x009917)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def patchouli(self, ctx):
        char = 'patchouli_knowledge'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xc646e0)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def youmu(self, ctx):
        char = 'konpaku_youmu'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x79eb50)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def koishi(self, ctx):
        char = 'komeiji_koishi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x62f500)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mokou(self, ctx):
        char = 'fujiwara_no_mokou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xf50000)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def satori(self, ctx):
        char = 'komeiji_satori'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xa700f5)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def wan(self, ctx):
        char = 'inubashiri_momiji'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def momiji(self, ctx):
        char = 'inubashiri_momiji'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def ran(self, ctx):
        char = 'yakumo_ran'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kagerou(self, ctx):
        char = 'imaizumi_kagerou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def reisen(self, ctx):
        char = 'reisen_udongein_inaba'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xf94aff)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def reisen2(self, ctx):
        char = 'reisen'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x2291ba)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def rei(self, ctx):
        char = 'reisen'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x2291ba)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def letty(self, ctx):
        char = 'letty_whiterock'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def remilia(self, ctx):
        char = 'remilia_scarlet'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xfd8cff)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def suwako(self, ctx):
        char = 'moriya_suwako'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def shizuha(self, ctx):
        char = 'aki_shizuha'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sanae(self, ctx):
        char = 'kochiya_sanae'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x24b343)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def clownpiece(self, ctx):
        char = 'clownpiece'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yukari(self, ctx):
        char = 'yakumo_yukari'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yuuka(self, ctx):
        char = 'kazami_yuuka'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x24b343)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def suika(self, ctx):
        char = 'ibuki_suika'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sekibanki(self, ctx):
        char = 'sekibanki'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def wriggle(self, ctx):
        char = 'wriggle_nightbug'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def hina(self, ctx):
        char = 'kagiyama_hina'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def alice(self, ctx):
        char = 'alice_margatroid'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kyouko(self, ctx):
        char = 'kasodani_kyouko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kisume(self, ctx):
        char = 'kisume'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def nazrin(self, ctx):
        char = 'nazrin'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sukuna(self, ctx):
        char = 'sukuna_shinmyoumaru'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kokoro(self, ctx):
        char = 'hata_no_kokoro'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yoshika(self, ctx):
        char = 'miyako_yoshika'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def seiga(self, ctx):
        char = 'kaku_seiga'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kogasa(self, ctx):
        char = 'tatara_kogasa'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def futo(self, ctx):
        char = 'mononobe_no_futo'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def miko(self, ctx):
        char = 'toyosatomimi_no_miko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mystia(self, ctx):
        char = 'mystia_lorelei'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xff8ade)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def genjii(self, ctx):
        char = 'genjii'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def byakuren(self, ctx):
        char = 'hijiri_byakuren'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x5b0082)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def hecatia(self, ctx):
        char = 'hecatia_lapislazuli'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x940f0f)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def junko(self, ctx):
        char = 'junko_(touhou)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xfbd55a)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Chang'e are you watching?")
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sagume(self, ctx):
        char = 'kishin_sagume'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xb4449c)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def doremy(self, ctx):
        char = 'doremy_sweet'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


					

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def minoriko(self, ctx):
        char = 'aki_minoriko'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yamame(self, ctx):
        char = 'kurodani_yamame'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)


					

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yuugi(self, ctx):
        char = 'hoshiguma_yuugi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def parsee(self, ctx):
        char = 'mizuhashi_parsee'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def tewi(self, ctx):
        char = 'inaba_tewi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xcc7c9c)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def medicine(self, ctx):
        char = 'medicine_melancholy'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def eiki(self, ctx):
        char = 'shiki_eiki'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x5b9c66)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def orin(self, ctx):
        char = 'kaenbyou_rin'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kaguya(self, ctx):
        char = 'houraisan_kaguya'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xef61ff)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def eirin(self, ctx):
        char = 'yagokoro_eirin'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kanako(self, ctx):
        char = 'yasaka_kanako'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x977cac)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def chen(self, ctx):
        char = 'chen'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




#this command seems to be unreliable
#switching to gelbooru to try and fix the issue
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def star(self, ctx):
        char = 'star_sapphire'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + 'gelbooru.com' + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char + '+rating:safe') as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    #source links are disabled because gel has NSFW ads
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def star2(self, ctx):
        char = 'star_sapphire'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def luna(self, ctx):
        char = 'luna_child'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def sunny(self, ctx):
        char = 'sunny_milk'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def eika(self, ctx):
        char = 'ebisu_eika'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def urumi(self, ctx):
        char = 'ushizaki_urumi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kutaka(self, ctx):
        char = 'niwatari_kutaka'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xdf9041)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def lunasa(self, ctx):
        char = 'lunasa_prismriver'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def lyrica(self, ctx):
        char = 'lyrica_prismriver'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def merlin(self, ctx):
        char = 'merlin_prismriver'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def prismriver(self, ctx):
        char = 'lunasa_prismriver+lyrica_prismriver+merlin_prismriver'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def moko(self, ctx):
        char = 'shangguan_feiying+fujiwara_no_mokou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Moko Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Artist: Shangguan Feiying")
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def gif(self, ctx):
        char = 'touhou+animated_gif'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklistgif + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='GIF Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="GIF Source: https://safebooru.org/index.php?page=post&s=view&id=" + sbooru_id)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def gif2(self, ctx):
        char = 'touhou+animated'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='GIF Image')
                    em.set_image(url=booruappend + msg)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def keiki(self, ctx):
        char = 'haniyasushin_keiki'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def saki(self, ctx):
        char = 'kurokoma_saki'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def mayumi(self, ctx):
        char = 'joutouguu_mayumi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def yachie(self, ctx):
        char = 'kicchou_yachie'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def ichirin(self, ctx):
        char = 'kumoi_ichirin'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def miyoi(self, ctx):
        char = 'okunoda_miyoi'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def chiyuri(self, ctx):
        char = 'kitashirakawa_chiyuri'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def pc98(self, ctx):
        char = 'touhou_(pc-98)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char) as r:
                if r.status == 200:
                    await asyncio.sleep(0.3)
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                        



#th_img_fan



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def youka(self, ctx):
        char = 'kazami_youka'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def kokuu(self, ctx):
        char = 'kokuu_haruto'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x14a625)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def ex_rumia(self, ctx):
        char = 'ex-rumia'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0xf5da42)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def hei(self, ctx):
        char = 'hei_meiling'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x88008c)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def flan_maman(self, ctx):
        char = 'flan-maman'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x8c0000)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
                    

#oj_img

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def oj(self, ctx):
        char = '100_percent_orange_juice'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def suguri(self, ctx):
        char = 'suguri_(character)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def saki_oj(self, ctx):
        char = 'saki_(suguri)'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                        pic = p[random.randint(0,99)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)
					

					


					

					
def setup(bot):
    bot.add_cog(ImageCog(bot))
