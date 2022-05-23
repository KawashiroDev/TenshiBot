#TenshiBot Image module v3(?)

#Based on TemmieGamerGuy's fix
#https://github.com/TemmieGamerGuy/TenshiBot/tree/fix

import discord
import requests
import aiohttp
#import praw
import lxml
import random
import asyncio
import twitter
import re

from discord.ext import commands
from bs4 import BeautifulSoup

#ignore certificate errors
#applies to the imagefetch function
ignorebadssl = True

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

boorublacklistgif = 'rating:general+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-audio+-webm+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron'

#tag blacklist v2

#base tags to apply to all levels (except gifs)
boorutags_base = 'solo+-rating:questionable+-rating:explicit+-6%2Bgirls+-comic+-greyscale+-huge_filesize+-animated+-audio+-webm+-absurdres+-monochrome'
#artists whose works slip by the tag filters
badartists = '+-nori_tamago+-shiraue_yuu+-hammer_(sunset_beach)+-roke_(taikodon)+-guard_bento_atsushi+-kushidama_minaka+-manarou+-shounen_(hogehoge)+-fusu_(a95101221)+-guard_vent_jun+-teoi_(good_chaos)+-wowoguni+-yadokari_genpachirou+-hydrant_(kasozama)+-e.o.+-fusu_(a95101221)+-nishiuri+-freeze-ex+-yuhito_(ablbex)+-koto_inari+-kurogarasu+-pokio'
#base tags for gif command
boorutags_gif = '-rating:questionable+-rating:explicit+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-6%2Bgirls+-comic+-greyscale+-bdsm+-huge_filesize+-lovestruck+-absurdres+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-audio+-webm+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nori_tamago+-nude+-butt_crack+-naked_apron+-what'
#default blacklisted tags (full SFW mode)
badtags_strict = "-rating:senstive+-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini+-spread_legs+-bdsm+-lovestruck+-artificial_vagina+-swimsuit+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-off_shoulder+-breast_hold+-cleavage+-nude+-butt_crack+-naked_apron+-convenient_censoring+-bra+-trapped+-restrained+-skirt_lift+-open_shirt+-underwear+-evil_smile+-evil_grin+-choker+-head_under_skirt+-skeleton+-open_fly+-o-ring_bikini+-middle_finger+-white_bloomers+-hot+-tank_top_lift+-short_shorts+-alternate_breast_size+-belly+-wind_lift+-you_gonna_get_raped+-convenient_leg+-convenient_arm+-downblouse+-torn_clothes+-sweater_lift+-open-chest_sweater+-bunnysuit+-gag+-gagged+-ball_gag+-hanging+-erect_nipples+-head_out_of_frame+-covering+-skirt_around_ankles+-furry+-shirt_lift+-vest_lift+-lifted_by_self+-when_you_see_it+-feet+-thighs+-skirt_hold+-open_dress+-open_clothes+-naked_shirt+-shirt_tug+-hip_vent+-no_panties+-surprised+-onsen+-naked_towel+-have_to_pee+-skirt_tug+-pole_dancing+-stripper_pole+-dimples_of_venus+-topless+-trembling+-no_humans+-creepy+-showgirl_skirt+-cookie_(touhou)+-pov+-fusion+-drugs+-weed+-forced_smile+-mouth_pull+-groin+-corruption+-dark_persona+-arms_behind_head+-crop_top+-gluteal_fold+-pregnant+-younger+-white_swimsuit+-tsundere+-crying+-naked_sheet+-undressing+-parody+-under_covers+-genderswap+-real_life_insert+-what+-confession+-race_queen+-naked_cloak+-latex+-bodysuit+-nazi+-swastika+-strap_slip+-chemise+-see-through+-dark+-bad_anatomy+-poorly_drawn+-messy+-you're_doing_it_wrong+-midriff+-large_breasts+-embarrassed+-smelling+-chains+-collar+-arms_up+-blurry_vision+-obese+-miniskirt+-leg_hold+-knees_to_chest+-knees_up+-clothes_pull+-giantess+-stepping+-shirtless+-3d+-smoking+-wall_slam+-noose+-4chan+-sheet_grab+-m_legs+-magnifying_glass+-fingering+-bandaid_on_pussy+-bandaids_on_nipples+-censored+-double_penetration+-erection+-group_sex+-double_handjob+-naizuri+-pasties+-penis+-sex+-pussy+-vaginal+-anal+-nipples+-aerolae+-large_areolae+-breasts_out+-breast_grab+-futanari+-implied_futanari+-condom+-condom_in_mouth+-cum+-used_condom"
#tags to blacklist in TenshiBot Hangout
badtags_hangout = '-sideboob+-pov_feet+-upskirt+-sexually_suggestive+-bdsm+-lovestruck+-artificial_vagina+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-seductive_smile+-no_bra+-breast_hold+-nude+-butt_crack+-naked_apron'
#tags to blacklist in moderate mode
badtags_moderate = '-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-bdsm+-lovestruck+-artificial_vagina+-covering_breasts+-huge_breasts+-blood+-penetration_gesture+-no_bra+-nude+-butt_crack+-naked_apron'
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


#text config
if booru == 'gelbooru.com':
    idtext = 'Gbooru ID'
    idtext_seija = 'pᴉ nɹooqƃ'
    idtext_sukuna = 'ᴳᵇᵒᵒʳᵘ ᴵᴰ'
if booru == 'safebooru.org':
    idtext = 'Sbooru ID'
    idtext_seija = 'pᴉ nɹooqs'
    idtext_sukuna = 'ˢᵇᵒᵒʳᵘ ᴵᴰ'

embedtitle = 'Character image'
embedtitle_jp = 'キャラクター画像'
    
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

    async def imagefetch(self, ctx, char, em, rng=1):
        if rng==1:
            score_rng = random.randint(0, 7)
            char = char + str(score_rng)
            #print(score_rng)
            #print("[Debug] Char has rng enabled")
        # check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(booruurl) as r:
                # print(booruurl)
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    #creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)


#landscape
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def testimage(self, ctx):
        
        sbooru_sauce = "[Source](http://reallylongurl2345678.com)"
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
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def testimage3(self, ctx, arg):
        
        sbooru_sauce = "http://example.com"
        sbooru_id = "123456"
        img_width = "1920"
        img_height = "1080"
        #file = discord.File("pics/test/kaga.jpg", filename="kaga.jpg")
        
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            embed_name = 'Test image (booru ID)'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            embed_name = 'Test image (booru ID)'
            
        em.set_author(name=embed_name)
        em.set_image(url=arg)
        em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
        em.add_field(name=idtext, value=sbooru_id, inline=True)
        em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
        #em.add_field(name="Creator ID", value=creator, inline=True)
        sbooru_img = await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def testimage4(self, ctx, arg):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = arg
        #check if Tenshi has a flag enabled or not
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + "id:" + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + "id:" + char
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
                    if "pixiv" in sbooru_sauce:
                        #if "img" in sbooru_sauce:
                            #extract pixiv id
                            #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce) 
                            #print (pixivid)
                            #reconstruct pixiv url
                            #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        #else:
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    #try to detect pixiv direct image links
                    #if "img" in sbooru_sauce:
                        #extract pixiv id
                        #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        #reconstruct pixiv url
                        #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    #else:
                        #sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + msg)
                    print("msg = " + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    #em.add_field(name="Creator ID", value=creator, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    async def genquery(self, ctx, char):
        booruurl = 'http://' + booru + '/index.php?page=post&s=list&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
        await ctx.send(booruurl)

    @commands.command()
    async def genquery2(self, ctx, char):
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
        print(booruurl)
        #await ctx.send(booruurl)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reimu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        char = 'Hakurei_Reimu+score:>='
        await self.imagefetch(ctx, char, em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def marisa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5e942)
        char = 'kirisame_marisa+score:>='
        await self.imagefetch(ctx, char, em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tenshi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hinanawi_tenshi+score:>='
        #print(ctx)
        #print(char)
        #print(em)
        await self.imagefetch(ctx, char, em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sakuya(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xc7c7c7)
        char = 'izayoi_sakuya+-id:5237460+score:>='
        await self.imagefetch(ctx, char, em)

                    
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def cirno(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x00e5ff)
        char = 'cirno+score:>='
        await self.imagefetch(ctx, char, em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def meiling(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x04b548)
        char = 'hong_meiling+score:>='
        await self.imagefetch(ctx, char, em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def flandre(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb50404)
        char = 'flandre_scarlet'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rumia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5da42)
        char = 'rumia'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rinnosuke(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'morichika_rinnosuke'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def murasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'murasa_minamitsu'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mamizou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'futatsuiwa_mamizou'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'toramaru_shou'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nemuno(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sakata_nemuno'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eternity(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'eternity_larva'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def narumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yatadera_narumi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def daiyousei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x04b548)
        char = 'daiyousei'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ringo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe2a81e)
        char = 'ringo_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kosuzu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'motoori_kosuzu'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def akyuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hieda_no_akyuu'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hatate(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb50480)
        char = 'himekaidou_hatate'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mima(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mima_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sariel(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sariel_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yumemi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'okazaki_yumemi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shinki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'shinki'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lily(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lily_white'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shion(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x048cb5)
        char = 'yorigami_shion'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def joon(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xaa4fa0)
        char = "yorigami_jo'on"
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seiran(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x6b87bd)
        char = 'seiran_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def koakuma(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x990000)
        char = 'koakuma'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def raiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xd25859)
        char = 'horikawa_raiko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def okina(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe69454)
        char = 'matara_okina'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mai(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x4e7764)
        char = 'teireida_mai'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satono(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe262b0)
        char = 'nishida_satono'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def aunn(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'komano_aun'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def komachi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xd25859)
        char = 'onozuka_komachi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wakasagihime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'wakasagihime'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def toyohime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x583b80)
        char = 'watatsuki_no_toyohime'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yorihime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xa84384)
        char = 'watatsuki_no_yorihime'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def renko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'usami_renko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def maribel(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'maribel_hearn'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nue(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x000000)
        char = 'houjuu_nue'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def iku(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'nagae_iku'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def elly(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'elly_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kasen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfb959e)
        char = 'ibaraki_kasen'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def keine(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x574b8c)
        char = 'kamishirasawa_keine'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def konngara(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'konngara'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuyuko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xff40d9)
        char = 'saigyouji_yuyuko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def aya(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe58a53)
        char = 'shameimaru_aya'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nitori(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb2daef)
        char = 'kawashiro_nitori'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sumireko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xaa6ad3)
        char = 'usami_sumireko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def okuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x009917)
        char = 'reiuji_utsuho'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def patchouli(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xc646e0)
        char = 'patchouli_knowledge'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def youmu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x79eb50)
        char = 'konpaku_youmu'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def koishi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x62f500)
        char = 'komeiji_koishi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mokou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf50000)
        char = 'fujiwara_no_mokou'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satori(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xa700f5)
        char = 'komeiji_satori'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wan(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'inubashiri_momiji'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def momiji(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'inubashiri_momiji'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ran(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yakumo_ran'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kagerou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'imaizumi_kagerou'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reisen(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0xf94aff)
        char = 'reisen_udongein_inaba+score:>=' + str(score_rng)
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def reisen2(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x2291ba)
        char = 'reisen'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x2291ba)
        char = 'reisen'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def letty(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'letty_whiterock'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def remilia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfd8cff)
        char = 'remilia_scarlet'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def suwako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'moriya_suwako'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def shizuha(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'aki_shizuha'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sanae(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x24b343)
        char = 'kochiya_sanae'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def clownpiece(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'clownpiece'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yukari(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yakumo_yukari'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuuka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x24b343)
        char = 'kazami_yuuka'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def suika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ibuki_suika'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sekibanki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sekibanki'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def wriggle(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'wriggle_nightbug'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hina(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kagiyama_hina'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def alice(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'alice_margatroid'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kyouko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kasodani_kyouko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kisume(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kisume'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def nazrin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'nazrin'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sukuna(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sukuna_shinmyoumaru+score:>=' + str(score_rng)
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'ᶜʰᵃʳᵃᶜᵗᵉʳ ᶦᵐᵃᵍᵉ'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="ᴵᵐᵃᵍᵉ ˢᵒᵘʳᶜᵉ", value=sbooru_sauce, inline=False)
                    em.add_field(name="ᴳᵇᵒᵒʳᵘ ᴵᴰ", value=sbooru_id, inline=True)
                    em.add_field(name="ᴰᶦᵐᵉⁿˢᶦᵒⁿˢ", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seija(self, ctx):
        score_rng = random.randint(0,5)
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kijin_seija+score:>=' + str(score_rng)
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'ǝƃɐɯI ɹǝʇɔɐɹɐɥƆ'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'pǝʇsᴉl ǝɔɹnos oN'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[ʌᴉxᴉԀ](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[ɹǝʇʇᴉʍʇ](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[oɔᴉNoɔᴉN](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[ʇɹ∀ʇuɐᴉʌǝp](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="ǝɔɹnos ǝƃɐɯI", value=sbooru_sauce, inline=False)
                    em.add_field(name="pI nɹooqפ", value=sbooru_id, inline=True)
                    em.add_field(name="suoᴉsuǝɯᴉp", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kokoro(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hata_no_kokoro'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yoshika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'miyako_yoshika'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def seiga(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kaku_seiga'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kogasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tatara_kogasa'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def futo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mononobe_no_futo'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def miko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'toyosatomimi_no_miko'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tojiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'soga_no_tojiko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mystia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xff8ade)
        char = 'mystia_lorelei'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def genjii(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'genjii_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def byakuren(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x5b0082)
        char = 'hijiri_byakuren'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hecatia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x940f0f)
        char = 'hecatia_lapislazuli'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def junko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xfbd55a)
        char = 'junko_(touhou)'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sagume(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xb4449c)
        char = 'kishin_sagume'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def doremy(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'doremy_sweet'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def minoriko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'aki_minoriko'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yamame(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kurodani_yamame'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuugi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hoshiguma_yuugi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def parsee(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'mizuhashi_parsee'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tewi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xcc7c9c)
        char = 'inaba_tewi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def medicine(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xe37f7d)
        char = 'medicine_melancholy'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eiki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x5b9c66)
        char = 'shiki_eiki'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def orin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kaenbyou_rin'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kaguya(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xef61ff)
        char = 'houraisan_kaguya'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eirin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'yagokoro_eirin'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kanako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x977cac)
        char = 'yasaka_kanako'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def chen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'chen'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def star(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'star_sapphire'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def luna(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'luna_child'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sunny(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'sunny_milk'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def eika(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ebisu_eika'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def urumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ushizaki_urumi'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kutaka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xdf9041)
        char = 'niwatari_kutaka'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lunasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lunasa_prismriver'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def lyrica(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lyrica_prismriver'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def merlin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'merlin_prismriver'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def prismriver(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'lunasa_prismriver+lyrica_prismriver+merlin_prismriver'
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + 'char'
        embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def moko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'jokanhiyou+fujiwara_no_mokou'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def moko2(self, ctx):
        embed_name = 'Moko image'
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'jokanhiyou+fujiwara_no_mokou'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
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
                    if "pixiv" in sbooru_sauce:
                        #if "img" in sbooru_sauce:
                            #extract pixiv id
                            #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce) 
                            #print (pixivid)
                            #reconstruct pixiv url
                            #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        #else:
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    #try to detect pixiv direct image links
                    #if "img" in sbooru_sauce:
                        #extract pixiv id
                        #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        #reconstruct pixiv url
                        #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    #else:
                        #sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
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
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_gif + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
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
                    #img_sauce = pic('source')
                    #if img_sauce == '':
                        #img_sauce = '[<source>No source listed</source>]'
                    #source_strip_start = str(img_sauce).strip('[<source>')
                    #sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #img_width = pic['width']
                    #img_height = pic['height']
                    #creator = pic['creator_id']
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='GIF Image')
                    em.set_image(url= raw_url + "if")
                    #await ctx.send(raw_url)
                    #await ctx.send(img_url)
                    em.add_field(name='Gbooru ID', value=sbooru_id, inline=True)
                    #em.set_footer(text="GIF Source: https://safebooru.org/index.php?page=post&s=view&id=" + sbooru_id)
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
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def saki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kurokoma_saki'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mayumi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'joutouguu_mayumi'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yachie(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kicchou_yachie'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ichirin(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kumoi_ichirin'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def miyoi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'okunoda_miyoi'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def chiyuri(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kitashirakawa_chiyuri'
        await self.imagefetch(ctx, char, em, 0)


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def pc98(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'touhou_(pc-98)'
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'Character image'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def satsuki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'satsuki_rin'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tokiko(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tokiko_(touhou)'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kotohime(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kotohime'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def rikako(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'asakura_rikako'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ruukoto(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ruukoto'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def elis(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'elis_(touhou)'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ellen(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'ellen'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def orange(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'orange_(touhou)'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def benben(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tsukumo_benben'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yatsuhashi(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tsukumo_yatsuhashi'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def mike(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xFEDAB8)
        char = 'goutokuji_mike'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def takane(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x6C9383)
        char = 'yamashiro_takane'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def sannyo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xC056C2)
        char = 'komakusa_sannyo'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def megumu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x2596BE)
        char = 'iizunamaru_megumu'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def chimata(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x5368AF)
        char = 'tenkyuu_chimata'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def tsukasa(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xE8DEE5)
        char = 'kudamaki_tsukasa'
        await self.imagefetch(ctx, char, em, 0)

        
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def momoyo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x28252B)
        char = 'himemushi_momoyo'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def misumaru(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'tamatsukuri_misumaru'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuuma(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x496DA9)
        char = 'toutetsu_yuuma'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def yuki(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x496DA9)
        char = 'yuki_(touhou)'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def fumo(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'fumo_(doll)'
        moderate_role = discord.utils.get(ctx.guild.roles, name="tenko_moderatemode")
        if moderate_role in ctx.guild.me.roles:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_moderate + '+' + char
            embed_name = 'ᗜˬᗜ'
            em.set_footer(text="Moderate mode is enabled on this server, image may not be SFW")
        else:
            booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char
            embed_name = 'ᗜˬᗜ'
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorutags_base + badtags_strict + badartists + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)


#th_img_fan



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def youka(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kazami_youka_(yokochu)'
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + boorublacklist + '+' + 'char'
        embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + badtags_strict + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kokuu(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kokuu_haruto'
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + 'char'
        embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + badtags_strict + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    #print(t)
                    p = t.find_all('post')
                    #print(p)
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    #creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ex_rumia(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5da42)
        char = 'ex-rumia'
        await self.imagefetch(ctx, char, em, 0)

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kokuu2(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0xf5da42)
        char = 'kokuu_haruto'
        await self.imagefetch(ctx, char, em, 0)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x88008c)
        char = 'hei_meiling'
        await self.imagefetch(ctx, char, em, 0)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def flan_maman(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x8c0000)
        char = 'flan-maman'
        await self.imagefetch(ctx, char, em, 0)
                    

#oj_img

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def oj(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = '100_percent_orange_juice'
        booruurl = 'http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + 'char'
        embed_name = 'Character image'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=' + badtags_strict + '+' + char) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num / 100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    #print(t)
                    p = t.find_all('post')
                    #print(p)
                    source = ((soup.find('post'))('source'))
                    if num < 100:
                        pic = p[random.randint(0, num - 1)]
                    elif page == maxpage:
                        pic = p[random.randint(0, 99)]
                    else:
                        pic = p[random.randint(0, 99)]
                    img_url = pic('file_url')
                    #for link in img_url:
                        #print(img_url.text)
                    #and cue the jankyness
                    #bs4 does have a way to do this
                    url_strip_start = str(img_url).strip('[<file_url>')
                    raw_url = str(url_strip_start).strip('</file_url>]')
                    #print(raw_url)
                    
                    img_id = pic('id')
                    id_strip_start = str(img_id).strip('[<id>')
                    sbooru_id = str(id_strip_start).strip('</id>]')
                    #print(sbooru_id)
                    
                    img_tags = pic('tags')
                    
                    img_sauce = pic('source')
                    if img_sauce == '':
                        img_sauce = '[<source>No source listed</source>]'
                    source_strip_start = str(img_sauce).strip('[<source>')
                    sbooru_sauce = str(source_strip_start).strip('</source>]')
                    #print(sbooru_sauce)
                    
                    # sbooru_sauce = "https://i.pximg.net/img-original/img/2020/12/25/18/14/37/86528174_p0.png"
                    img_width = pic('width')
                    
                    width_strip_start = str(img_width).strip('[<width>')
                    width = str(width_strip_start).strip('</width>]')
                    
                    img_height = pic('height')
                    height_strip_start = str(img_height).strip('[<height>')
                    height = str(height_strip_start).strip('</height>]')
                    
                    #creator = pic('creator_id')
                    if sbooru_sauce == '':
                        sbooru_sauce = 'No source listed'
                    if "hentai" in sbooru_sauce:
                        sbooru_sauce = "Source hidden\n(NSFW website)"
                    if "pixiv" in sbooru_sauce:
                        # if "img" in sbooru_sauce:
                        # extract pixiv id
                        # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        # print (pixivid)
                        # reconstruct pixiv url
                        # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        # else:
                        # sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    # try to detect pixiv direct image links
                    # if "img" in sbooru_sauce:
                    # extract pixiv id
                    # pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                    # check if there's an actual pixiv id in the source link or not
                    # if pixivid == "":
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # else:
                    # reconstruct pixiv url
                    # sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    # else:
                    # sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    # em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name=embed_name)
                    em.set_image(url=booruappend + str(raw_url))
                    em.add_field(name="Image Source", value=sbooru_sauce, inline=False)
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=str(width) + "x" + str(height), inline=True)
                    # em.add_field(name="RNG", value=score_rng, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)
					
					
					
    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def suguri(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'suguri_(character)'
        await self.imagefetch(ctx, char, em, 0)




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
                    if "pixiv" in sbooru_sauce:
                        #if "img" in sbooru_sauce:
                            #extract pixiv id
                            #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce) 
                            #print (pixivid)
                            #reconstruct pixiv url
                            #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                        #else:
                        sbooru_sauce = "[Pixiv](" + sbooru_sauce + ")"
                    if "twitter" in sbooru_sauce:
                        sbooru_sauce = "[Twitter](" + sbooru_sauce + ")"
                    if "nicovideo" in sbooru_sauce:
                        sbooru_sauce = "[NicoNico](" + sbooru_sauce + ")"
                    if "deviantart" in sbooru_sauce:
                        sbooru_sauce = "[DeviantArt](" + sbooru_sauce + ")"
                    #try to detect pixiv direct image links
                    #if "img" in sbooru_sauce:
                        #extract pixiv id
                        #pixivid = re.search('(?<!\d)(\d{8})(?!\d)', sbooru_sauce)
                        #reconstruct pixiv url
                        #sbooru_sauce = "[Pixiv](http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + pixivid.group(1) + ")"
                    #else:
                        #sbooru_sauce = "[Source](" + sbooru_sauce + ")"
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em = discord.Embed(title='', description=' ', colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name="Character image")
                    em.set_image(url=booruappend + msg)
                    em.add_field(name="Image source", value=sbooru_sauce, inline=False)    
                    em.add_field(name=idtext, value=sbooru_id, inline=True)
                    em.add_field(name="Dimensions", value=img_width + "x" + img_height, inline=True)
                    await asyncio.sleep(0.15)
                    sbooru_img = await ctx.send(embed=em)
					
#kantai_img




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kongou(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kongou_(kantai_collection)'
        await self.imagefetch(ctx, char, em, 0)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def haruna(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'haruna_(kantai_collection)'
        await self.imagefetch(ctx, char, em, 0)




    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def hiei(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'hiei_(kantai_collection)'
        await self.imagefetch(ctx, char, em, 0)



    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def kirishima(self, ctx):
        em = discord.Embed(title='', description=' ', colour=0x42D4F4)
        char = 'kirishima_(kantai_collection)'
        await self.imagefetch(ctx, char, em, 0)


					

					
def setup(bot):
    bot.add_cog(ImageCog(bot))
