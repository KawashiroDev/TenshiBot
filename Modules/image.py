#TenshiBot Image module

import discord
import requests
import aiohttp
#import praw
import lxml
import random
import asyncio
import twitter

from discord.ext import commands
from bs4 import BeautifulSoup

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

#if adding stuff to the blacklist, add it to the v2 section and not this
boorublacklist = 'rating:safe+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-animated+-audio+-webm+rating:safe+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron'

boorublacklistgif = 'rating:safe+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-audio+-webm+rating:safe+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron'

#tag blacklist v2

#base tags to apply to all levels (except gifs)
boorutags_base = 'solo+rating:safe+-6%2Bgirls+-comic+-greyscale+-huge_filesize+-animated+-audio+-webm+-absurdres+-monochrome'
#artists whose works slip by the tag filters
badartists = '+-nori_tamago+-shiraue_yuu+-hammer_(sunset_beach)+-roke_(taikodon)+-guard_bento_atsushi+-kushidama_minaka+-manarou+-shounen_(hogehoge)+-fusu_(a95101221)+-guard_vent_jun+-teoi_(good_chaos)+-wowoguni+-yadokari_genpachirou+-hydrant_(kasozama)+-e.o.+-fusu_(a95101221)+-nishiuri'
#base tags for gif command
boorutags_gif = 'rating:safe+-6%2Bgirls+-comic+-greyscale+-huge_filesize+-audio+-webm+-absurdres'
#default blacklisted tags (full SFW mode)
badtags_strict = "-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-spread_legs+-bdsm+-lovestruck+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nude+-butt_crack+-naked_apron+-convenient_censoring+-bra+-trapped+-restrained+-skirt_lift+-open_shirt+-underwear+-evil_smile+-evil_grin+-choker+-head_under_skirt+-skeleton+-open_fly+-o-ring_bikini+-middle_finger+-white_bloomers+-hot+-tank_top_lift+-short_shorts+-alternate_breast_size+-belly+-wind_lift+-you_gonna_get_raped+-convenient_leg+-convenient_arm+-downblouse+-torn_clothes+-sweater_lift+-open-chest_sweater+-bunnysuit+-gag+-gagged+-ball_gag+-hanging+-erect_nipples+-head_out_of_frame+-covering+-skirt_around_ankles+-furry+-shirt_lift+-vest_lift+-lifted_by_self+-when_you_see_it+-feet+-thighs+-skirt_hold+-open_dress+-open_clothes+-naked_shirt+-shirt_tug+-hip_vent+-no_panties+-surprised+-onsen+-naked_towel+-have_to_pee+-skirt_tug+-pole_dancing+-stripper_pole+-dimples_of_venus+-topless+-trembling+-no_humans+-creepy+-showgirl_skirt+-cookie_(touhou)+-pov+-fusion+-drugs+-weed+-forced_smile+-mouth_pull+-groin+-corruption+-dark_persona+-arms_behind_head+-crop_top+-gluteal_fold+-pregnant+-younger+-white_swimsuit+-tsundere+-crying+-naked_sheet+-undressing+-parody+-under_covers+-genderswap+-real_life_insert+-what+-confession+-race_queen+-naked_cloak+-latex+-bodysuit+-nazi+-swastika+-strap_slip+-chemise+-see-through+-dark+-bad_anatomy+-poorly_drawn+-messy+-you're_doing_it_wrong+-midriff+-large_breasts+-embarrassed+-smelling"
#tags to blacklist in TenshiBot Hangout
badtags_hangout = '-sideboob+-pov_feet+-upskirt+-sexually_suggestive+-bdsm+-lovestruck+-artificial_vagina+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-breast_hold+-nude+-butt_crack+-naked_apron'
#tags to blacklist in moderate mode
badtags_moderate = '-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-bdsm+-lovestruck+-artificial_vagina+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-breast_hold+-nude+-butt_crack+-naked_apron'
#tags to blacklist in an NSFW channel
badtags_nsfwmode = ''

#image shuffler queries (experimental!, may return questionable images)
last_updated = "+sort:updated:desc"
random_hq = "+sort:random+score:>=10"

#not used
randomsort = "+sort:random"
minscore = "score:>=0"
sorting = "sort:updated:desc"
startpage = "&pid=42"
#+sort:random:123

#rng stuff
score_rng_max = "5"
#score_rng = random.randint(0,5)

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
#safebooru URL's used to need http added to the start but now they dont anymore
booruappend = ''

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 3
#timeframe (seconds)
rlimit_time = 10
#

#patreon nag text
patreonnag = "patreonnag text"

#general footer
normalfooter = "todo:put something here"

footer = [
normalfooter,
normalfooter,     
normalfooter,
normalfooter,
patreonnag,
]

if booru == 'gelbooru.com':
    idtext = 'Gbooru ID'
if booru == 'safebooru.org':
    idtext = 'Sbooru ID'
    
keiki_title = [
"Character image",
"Create!",     
"Oh!",
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

#landscape
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def testimage(self, ctx):
        
        sbooru_sauce = "http://example.com"
        sbooru_id = "123456"
        img_width = "1920"
        img_height = "1080"
        file = discord.File("pics/test/dev_fumo.jpg", filename="dev_fumo.jpg")
        
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            embed_name = 'Test image (l)'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            embed_name = 'Test image (l)'
            
        em.set_author(name=embed_name)
        em.set_image(url="attachment://dev_fumo.jpg")
        em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
        em.add_field(name=idtext, value=sbooru_id, inline=True)
        em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
        #em.add_field(name="Creator ID", value=creator, inline=True)
        sbooru_img = await ctx.send(file=file, embed=em)


#portrait
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def testimage2(self, ctx):
        
        sbooru_sauce = "http://example.com"
        sbooru_id = "123456"
        img_width = "1920"
        img_height = "1080"
        file = discord.File("pics/test/kaga.jpg", filename="kaga.jpg")
        
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            embed_name = 'Test image (p)'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            embed_name = 'Test image (p)'
            
        em.set_author(name=embed_name)
        em.set_image(url="attachment://kaga.jpg")
        em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
        em.add_field(name=idtext, value=sbooru_id, inline=True)
        em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
        #em.add_field(name="Creator ID", value=creator, inline=True)
        sbooru_img = await ctx.send(file=file, embed=em)



    @commands.command()
    async def genquery(self, ctx, char):
        booruurl = 'http://' + booru + '/index.php?page=post&s=list&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
        await ctx.send(booruurl)

    @commands.command()
    async def genquery2(self, ctx, char):
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
        await ctx.send(booruurl)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reimu(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        char = 'Hakurei_Reimu+score:>=' + str(score_rng)
        print(score_rng)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
                #print(booruurl)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    em.add_field(name="RNG", value=score_rng, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)  
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def marisa(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0xf5e942)
        char = 'kirisame_marisa+score:>=' + str(score_rng)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    em.add_field(name="RNG", value=score_rng, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hinanawi_tenshi+score:>=' + str(score_rng)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    em.add_field(name="RNG", value=score_rng, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi_react(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hinanawi_tenshi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



                        



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi2(self, ctx):
        em = discord.Embed(title='', description='' + source, colour=0x42D4F4)
        char = 'hinanawi_tenshi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    msg2 = pic['change']
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    await ctx.send(msg)
                    await ctx.send('img_source:' + source)
                    await ctx.send(str(pic))
                    print(pic)
                    print(msg2)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi3(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        #define the character tag
        char = 'hinanawi_tenshi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi4(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hinanawi_tenshi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            #em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    sbooru_id = pic['id']
                    sbooru_tags = pic['tags']
                    sbooru_sauce = pic['source']
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_footer(text=random.choice(footer))
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sakuya(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0xc7c7c7)
        char = 'izayoi_sakuya+-id:5237460+score:>=' + str(score_rng)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    em.add_field(name="RNG", value=score_rng, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)

                    
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def cirno(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0x00e5ff)
        char = 'cirno+score:>=' + str(score_rng)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    em.add_field(name="RNG", value=score_rng, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def meiling(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x04b548)
        char = 'hong_meiling'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def flandre(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        char = 'flandre_scarlet'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rumia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5da42)
        char = 'rumia'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rinnosuke(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'morichika_rinnosuke'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def murasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'murasa_minamitsu'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
					

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mamizou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'futatsuiwa_mamizou'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
					




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'toramaru_shou'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nemuno(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sakata_nemuno'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eternity(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'eternity_larva'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
					




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def narumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yatadera_narumi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def daiyousei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x04b548)
        char = 'daiyousei'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ringo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe2a81e)
        char = 'ringo_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kosuzu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'motoori_kosuzu'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def akyuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hieda_no_akyuu'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hatate(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb50480)
        char = 'himekaidou_hatate'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mima(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mima_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sariel(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sariel_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yumemi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'okazaki_yumemi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shinki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'shinki'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                        



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lily(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lily_white'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shion(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x048cb5)
        char = 'yorigami_shion'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def joon(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xaa4fa0)
        char = "yorigami_jo'on"
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seiran(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x6b87bd)
        char = 'seiran_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def koakuma(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x990000)
        char = 'koakuma'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def raiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xd25859)
        char = 'horikawa_raiko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def okina(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe69454)
        char = 'matara_okina'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mai(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x4e7764)
        char = 'teireida_mai'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satono(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe262b0)
        char = 'nishida_satono'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def aunn(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'komano_aun'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def komachi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xd25859)
        char = 'onozuka_komachi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wakasagihime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'wakasagihime'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seija(self, ctx):
        char = 'kijin_seija'
        em = discord.Embed(title='', description=' ', colour=0xaeb4c6)
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ')
                    em.set_image(url=booruappend + msg)
                    sbooru_img = await ctx.send(embed=em)
                    #fix




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def toyohime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x583b80)
        char = 'watatsuki_no_toyohime'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yorihime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xa84384)
        char = 'watatsuki_no_yorihime'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def renko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'usami_renko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def maribel(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'maribel_hearn'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nue(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x000000)
        char = 'houjuu_nue'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def iku(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'nagae_iku'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def elly(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'elly_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kasen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfb959e)
        char = 'ibaraki_kasen'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def keine(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x574b8c)
        char = 'kamishirasawa_keine'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def konngara(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'konngara'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuyuko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xff40d9)
        char = 'saigyouji_yuyuko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def aya(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe58a53)
        char = 'shameimaru_aya'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nitori(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb2daef)
        char = 'kawashiro_nitori'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sumireko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xaa6ad3)
        char = 'usami_sumireko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def okuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x009917)
        char = 'reiuji_utsuho'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def patchouli(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xc646e0)
        char = 'patchouli_knowledge'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def youmu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x79eb50)
        char = 'konpaku_youmu'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def koishi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x62f500)
        char = 'komeiji_koishi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mokou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf50000)
        char = 'fujiwara_no_mokou'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satori(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xa700f5)
        char = 'komeiji_satori'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wan(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'inubashiri_momiji'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def momiji(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'inubashiri_momiji'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ran(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yakumo_ran'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kagerou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'imaizumi_kagerou'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reisen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf94aff)
        char = 'reisen_udongein_inaba'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reisen2(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x2291ba)
        char = 'reisen'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x2291ba)
        char = 'reisen'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def letty(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'letty_whiterock'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def remilia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfd8cff)
        char = 'remilia_scarlet'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def suwako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'moriya_suwako'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shizuha(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'aki_shizuha'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sanae(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x24b343)
        char = 'kochiya_sanae'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def clownpiece(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'clownpiece'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yukari(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yakumo_yukari'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuuka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x24b343)
        char = 'kazami_yuuka'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def suika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ibuki_suika'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sekibanki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sekibanki'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wriggle(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'wriggle_nightbug'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hina(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kagiyama_hina'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def alice(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'alice_margatroid'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kyouko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kasodani_kyouko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kisume(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kisume'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nazrin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'nazrin'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sukuna(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sukuna_shinmyoumaru'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kokoro(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hata_no_kokoro'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yoshika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'miyako_yoshika'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seiga(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kaku_seiga'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kogasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tatara_kogasa'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def futo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mononobe_no_futo'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def miko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'toyosatomimi_no_miko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tojiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'soga_no_tojiko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mystia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xff8ade)
        char = 'mystia_lorelei'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def genjii(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'genjii_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def byakuren(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x5b0082)
        char = 'hijiri_byakuren'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hecatia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x940f0f)
        char = 'hecatia_lapislazuli'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def junko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfbd55a)
        char = 'junko_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char + '+-bofeng'
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Chang'e are you watching?")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.set_footer(text="Image Source: " + sbooru_sauce)    
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sagume(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb4449c)
        char = 'kishin_sagume'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def doremy(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'doremy_sweet'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


					

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def minoriko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'aki_minoriko'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yamame(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kurodani_yamame'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


					

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuugi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hoshiguma_yuugi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def parsee(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mizuhashi_parsee'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tewi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xcc7c9c)
        char = 'inaba_tewi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def medicine(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe37f7d)
        char = 'medicine_melancholy'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eiki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x5b9c66)
        char = 'shiki_eiki'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def orin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kaenbyou_rin'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kaguya(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xef61ff)
        char = 'houraisan_kaguya'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eirin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yagokoro_eirin'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kanako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x977cac)
        char = 'yasaka_kanako'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def chen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'chen'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def star(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'star_sapphire'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def star2(self, ctx):
        char = 'star_sapphire'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def luna(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'luna_child'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sunny(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sunny_milk'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ebisu_eika'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def urumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ushizaki_urumi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kutaka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xdf9041)
        char = 'niwatari_kutaka'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lunasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lunasa_prismriver'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lyrica(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lyrica_prismriver'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def merlin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'merlin_prismriver'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def prismriver(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lunasa_prismriver+lyrica_prismriver+merlin_prismriver'
        embed_name = 'Character image'
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def moko(self, ctx):
        embed_name = 'Moko image'
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'jokanhiyou+fujiwara_no_mokou'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + 'gelbooru.com' + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + char) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name='Gbooru ID', value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='GIF Image')
                    em.set_image(url=booruappend + msg)
                    em.set_footer(text="GIF Source: https://safebooru.org/index.php?page=post&s=view&id=" + sbooru_id)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='GIF Image')
                    em.set_image(url=booruappend + msg)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def keiki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'haniyasushin_keiki'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = text=random.choice(keiki_title)
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = text=random.choice(keiki_title)
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def saki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kurokoma_saki'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mayumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'joutouguu_mayumi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yachie(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kicchou_yachie'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ichirin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kumoi_ichirin'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def miyoi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'okunoda_miyoi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def chiyuri(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kitashirakawa_chiyuri'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)





    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def pc98(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'touhou_(pc-98)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satsuki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'satsuki_rin'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tokiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tokiko_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mimiqwertyuiop(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mimi-chan'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kotohime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kotohime'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                        



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rikako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'asakura_rikako'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ruukoto(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ruukoto'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def elis(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'elis_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ellen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ellen'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def orange(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfDBE3B)
        char = 'orange_(touhou)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def benben(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tsukumo_benben'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)                    




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yatsuhashi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tsukumo_yatsuhashi'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


#th_img_fan



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def youka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character image')
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kokuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x14a625)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Character image')
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ex_rumia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5da42)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x88008c)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def flan_maman(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x8c0000)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
                    

#oj_img

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)

					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)
					
#kantai_img




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kongou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kongou_(kantai_collection)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def haruna(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'haruna_(kantai_collection)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hiei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hiei_(kantai_collection)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kirishima(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kirishima_(kantai_collection)'
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession() as session:
            async with session.get(booruurl) as r:
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
                    img_width = pic['width']
                    img_height = pic['height']
                    creator = pic['creator_id']
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    sbooru_img = await ctx.send(embed=em)


					

					
def setup(bot):
    bot.add_cog(ImageCog(bot))
