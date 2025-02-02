#TenshiBot Slipstream version
#Created by KawashiroDev


##Parameters##

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '2.6.3'

#Owner ID
ownerid = 166189271244472320

#hangout ID
hangoutid = 273086604866748426

#Patreon role ID
patreonrole = 367069832405057546

#YT membership role ID
yt_member = 454051781371232291

#needed for slash commands?
#guild_ids = [273086604866748426]

#Limited network mode
#enable to reduce Tenshi's data usage if running on slow wifi or 3g/4g
limit_net = False

#DM on boot (production only)a
bootdm = True

#Smart DM on boot
#enable to not send a DM if on_ready() was called without a reboot command being used
smartboot = False

#DM on error
errordm = True

#Ghost mode
#enable to run on Tenshi's production account but respond to a different prefix to not clash with the server instance
#set prefix: =tb <command>
ghost = False

#commands to show in the help sections
#general
gen_command = "About, Support, Help, KoFi, Patreon, Messagedev <message>"
#fun
fun_command = "Hooray, F, Confused"
#image
img_command = "Safebooru <query>, Gif, Honk"
#debug
dbug_command = "debug"
#touhou characters
char_toho = "Reimu"
#oj characters
char_oj = "Suguri"
#kantai characters
char_kantai = "Haruna"

#Sound on boot (debug only)
bootsound = True

#windows check
#if this directory exists then run in debug mode
#if not then run in production mode
win_dir_check = '/windows'

#Spicetools URL
spiceURL = "http://onlyone.cab/downloads/spicetools-latest.zip"

#Ollama config (tenshichat command)
#URL
ollamaurl = "http://haruhi:11434/api/generate"
#Model
chatmodel = "llama3.2"

import discord
#import requests
import aiohttp
import random
import asyncio
import os
import subprocess
#import cleverbot_io
import time
#import Cleverbotio
import traceback
#import praw
import lxml
#import saucenaopy
#import twitter
import datetime
#import playsound
import async_cleverbot as ac
import sys
import glob
import zipfile
import shutil
import hashlib
import contextlib
import io
import logging
import setproctitle
import psutil
import json


from discord.ext import commands
#from discord.commands import slash_command
from random import randint
from bs4 import BeautifulSoup
from urlextract import URLExtract
#from Cleverbotio import 'async' as cleverbot
#from saucenaopy import SauceNAO
from datetime import datetime, timedelta, timezone
#from playsound import playsound
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory
#from github import Github
from zipfile import ZipFile
#from discord_slash import SlashCommand, SlashContext
#from discord_slash.utils.manage_components import create_button, create_actionrow
#from discord_slash.model import ButtonStyle
#from text_to_speech import speak
#from ollama import chat
#from ollama import ChatResponse
#from ollama import AsyncClient

#https://www.microsoft.com/en-us/download/details.aspx?id=48159
from profanityfilter import ProfanityFilter

print('[Startup] Please wait warmly...')

#change process title
setproctitle.setproctitle('Tenshi')

#start logging console
#sys.stdout = open("test.txt", "w")
#print('test')


#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)


pf = ProfanityFilter()

#Windows or linux check
#used to autoswitch the bot between debug/production modes

if (os.path.isdir(win_dir_check)) == True:
    print('[Startup] Detected a windows PC, running in debug mode')
    bot_mode = 'Debug'
    debugmode = True
    initial_extensions = ['Modules.image', 'Modules.booru', 'Modules.debug', 'Modules.messaging']#, 'Modules.cleverbot']#, 'Modules.slash_cmd']
    print('[Debug] /Modules/debug.py loaded')
    print('')
    print('Welcome to CelestialOS 98...')
    if bootsound == False:
        print('Loading program: TenshiBot.exe')
    if bootsound == True:
        #playsound('Startup_98.wav', False)
        print('Loading program: TenshiBot.exe')
    
if ghost == True:
    print('[Startup] Running in ghost mode')
    bot_mode = 'Ghost'
    debugmode = False
    initial_extensions = ['Modules.image', 'Modules.booru', 'Modules.twitter', 'Modules.messaging']#, 'Modules.cleverbot']

if (os.path.isdir(win_dir_check)) == False:
    print('[Startup] Running in production mode')
    bot_mode = 'Production'
    debugmode = False
    initial_extensions = ['Modules.image', 'Modules.booru', 'Modules.messaging']#, 'Modules.cleverbot']#, 'Modules.slash_cmd']

test = "test"

staring_satori = discord.File('pics/satori_stare.jpg')


mentioned_nomsg = [
"Hm..",
"You want something?",
"Yes?",
"Peaches are delicious, you should try one sometime",
"In Soviet Russia, bot tags you",
"(￣ω￣;)",
"¡ǝɹǝɥ sɐʍ ɐɾᴉǝS",
"You picked the wrong heaven fool!",
"A red spy is in the base?!",
"Eh?!, some MrBeast guy just gave Shion ¥100,000",
#"You seen John Connor around here?",
#"CrashOverride? What kind of username is that?",
#"ZeroCool? Sounds like one of Cirno's aliases",
"Wait... Yukari is here?",
"Chang'e are you watching? \nSome fox lady said hi",
"Hold on a sec i just saw Sakuya with some coffee",
"Guys the thermal drill, go get it",
"Am i a joke to you?",
"You do not spark joy",
#"I am inevitable",
#"You can't do anything so don't even try, get some help. Don't do what Sonic does \n **Sonic, dead or alive is mine**",
"!",
"!!",
"?!",
"That's not it!",
"Da Ze~... or whatever Marisa usually says",
#"Did you know that Hector is gonna be running three Honda Civics with Spoon engines.",
"Don’t let this distract you from the fact that Hector is going to be running three Honda civics with spoon engines, and on top of that, he just went into Harry’s and bought three t66 turbos with NOS, and a motec exhaust system."
"Do you have time to talk about our lord and saviour Byakuren?",
"Greetings Professor Falken.",
"Shall we play a game?",



"*Stares*",
"*Looks around*",
"*Stares at you*",
#"*Eating a peach~*",
"*Is eating a peach~*",
"*Is eating a corndog~*",
"*Is looking at Shion~*",
"*Is cuddling Shion~*",
"*Is playing with Shion's hair~*",
"*Looks away*",
"*Is watching RWBY~*",
"*Zzz...*",
#"U+1F351",
"*Humming Wonderful Heaven~*",
"*Humming Flowering Night~*",
#"Hack the planet",

"*♪Nagareteku toki no naka de demo kedarusa ga hora guruguru mawatte♪*",
"*♪Blushing faces covered in pink♪\n♪Rushing bombs, exploding ink!♪*",
"*♪Too many shadows whispering voices♪\n♪Faces on posters too many choices♪*",
"*♪Lights and any more♪*",
"*♪Let's move into the brand new world♪\n♪Let's dive into the brand new trip♪*",
"*♪Running in the 90's♪\n♪It's a new way to set me free♪*",
"♪Freedom is... *invisible*♪",
"♪*I'll never find the sound of silence*♪",
"♪*Stay where you are~*♪",
"♪*Take my hand we drift away♪\n♪To a place beyond the stars♪*",
]

mentioned_nomsg_penny = [
"Salutations",     
"Salutations!",    
"Salutations, Meat person",
"Hello meat person",
]

mentioned_nomsg_christmas = [
"?",     
"Hi?",    
"Merry Christmas!",
"Ooh, it's that time of year isn't it?",
"Ah, that reminds me. I should make it snow",
"♪*Jingle bells\nYukari smells♪",
"*Is humming I wish it could be christmas everyday~*",
]

mentioned_nomsg_halloween = [
"Trick or treat!",     
"!!",    
"Spooky scary skeletons",
"*Is carving a pumpkin~*",
"♪*He did the mash, he did the monster mash*♪",
"Aaah a spider!",
"♪*Ooo eee ooo ah ah ting tang walla walla bing bang*♪",
]

shuffle_test = [
"avatars/test/1.png",
"avatars/test/2.png",
"avatars/test/3.png",
"avatars/test/4.png",
]

playingstatus = [
"TenshiBot",
"with Iku",
"with the weather",
"Touhou Hisoutensoku",
"Touhou SWR",
"Team Fortress 2",
]

playingstatus_console = [
"Magnavox Odyssey",
"Atari 2600",
"Playstation 1",
"Playstation 2",
"SouljaGame",
"Nintendo Switch",
"Nintendo DS",
"Game Boy Advance",
"PSVita",
"Sega RingEdge",
"Taito Type X",
"GPD Win" #rip my Win 2
"GPD Win Max"
"Smach Z" #rip smach z 2015(?)-2021
"Steam Deck"
]

scamlinks = [
"http://dlscord.app/airdrop/nitro",
"https://dlscord.org/airdrop/nitro",
" https://dlscord ",
]

food = [
    "🍑",
    "🍪",
    "🍣",
    "🍟",
    "🍕",
    "🍚",
    "🍇",
    "🍓",
    "🍔",
    "🍰",
    "🍄",
    "🍡",
    "🍛",
    "🌵",
    "🍜",
    "🌽",
    "🍬",
    "🍋",
    "🍹",
    "🍝",
    "🍮",
    "🎂",
    "🍏",
    "🍈",
    "🍠",
    "☕",
    "🍺",
    "🍷",
    "🍥",
    "🥚",
    "🍨",
    "🍭",
    "🍊",
    "🍉",
    "🍞",
    "🍍",
    "🍘",
    "🍧"
]

#define intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

debugintents = discord.Intents.default()
debugintents.typing = True
debugintents.presences = True
debugintents.members = True
debugintents.message_content = True

#Disable sharding and = prefix if in debug mode
#if you want to have the bot run as normal on a windows machine then change the windows folder check to a non existent folder
if ghost == True:
    bot = commands.AutoShardedBot(command_prefix=('=='), case_insensitive=True, shard_count=3, intents=intents)
    
if debugmode == True:
    bot = commands.Bot(command_prefix=commands.when_mentioned, case_insensitive=True, intents=debugintents)
#    slash = SlashCommand(bot, sync_commands=True)

else:
    bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('='), case_insensitive=True, shard_count=4, intents=intents)
    
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
bot.remove_command("help")

#Sharding! should help with performance since the bot is on 1000+ servers
#client = discord.AutoShardedClient()
#client = discord.Client()

st = time.time()

pf = ProfanityFilter()

#git = open("Tokens/github.txt", "r")
#git_token = git.read()
#g = Github(git_token)


#url extractor stuff
extractor = URLExtract()

#saucenao api stuff
#saucekey = open("Tokens/sn_api.txt", "r")
#sn_key = saucekey.read()
#sn = SauceNAO(sn_key)

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)



#Discordbots.org API stuff
#if in debug mode then open a blank token file which will cause the server count
#to not be posted because i don't want the debug acc posting it's server count
if debugmode == True:        
    tkn_dbl = open("Tokens/dbl_api_blank.txt", "r")
else:
    tkn_dbl = open("Tokens/dbl_api.txt", "r")
token_dbl = tkn_dbl.read()
tkn_dbl.close() 
dbltoken = token_dbl
url_dbl = ("https://top.gg/api/bots/252442396879486976/stats")
headers_dbl = {"Authorization" : dbltoken}

if debugmode == True:        
    tkn_dbo = open("Tokens/dbo_api.txt", "r")
else:
    tkn_dbo = open("Tokens/dbo_api.txt", "r")
token_dbo = tkn_dbo.read()
tkn_dbo.close() 
dbotoken = token_dbo
url_dbo = ("https://discord.bots.gg/api/v1/bots/252442396879486976/stats")
headers_dbo = {"Authorization" : dbotoken}


@bot.event
async def on_ready():
    yuyuko = await bot.fetch_user(ownerid)
    #print(yuyuko)

    if debugmode == True:
        print(' ')
        print('TenshiBot ' + bot_version + ' (Debug mode) initialized')
        print('User ID:  ' + str(bot.user.id))
        await bot.change_presence(activity=discord.Game(name="TB [" + bot_version + "] (D)"))
        #await yuyuko.send("System ready!")
        print(' ')
        #payload = {"guildCount"  : str(len(bot.guilds))}
        #payload_dbo = {"guildCount"  : int(1800)}
        #async with aiohttp.ClientSession() as aioclient:
        #    await aioclient.post(url_dbo, data=payload_dbo, headers=headers_dbo)
        return

    if smartboot == True:
        print("[debug] smart boot enabled")
        if os.path.isfile('reboot.tenko'):
            os.remove("reboot.tenko")
            print('TenshiBot ' + bot_version + ' initialized')
            await yuyuko.send("System ready!")
            await bot.change_presence(activity=discord.Game(name=random.choice(playingstatus)))
            return
        else:
            print("[debug] on_ready was called but the server/bot didn't reboot, ignoring")
            #blank status fix
            await bot.change_presence(activity=discord.Game(name=random.choice(playingstatus)))
            return
        
    if ghost == True:
        await yuyuko.send("System ready! (running in ghost mode)")
        print('TenshiBot startup complete ')
        print(discord.version_info)
        return
    
    else:
        await yuyuko.send("System ready!")
        
        print(' ')
        print('TenshiBot startup complete ')
        print(' ')
        print('User ID - ' + str(bot.user.id))
        print('Username - ' + bot.user.name)
        print('Shard Count - ' + str(bot.shard_count))
        print('TenshiBot Ver - ' + bot_version)
        print('System Mode - ' + bot_mode)
        print(' ')
        print('servercount - ' + str(len(bot.guilds)))
        print(discord.version_info)
        payload_dbl = {"server_count"  : str(len(bot.guilds))}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url_dbl, data=payload_dbl, headers=headers_dbl)
        await bot.change_presence(activity=discord.Game(name="TB [" + bot_version + "]"))
        await asyncio.sleep(5)
        #await bot.change_presence(activity=discord.Game(name="Startup complete"))
        #await asyncio.sleep(5)
        #await bot.change_presence(activity=discord.Streaming(name="TenshiBot", url='https://twitch.tv/99710'))
        await bot.change_presence(activity=discord.Game(name=random.choice(playingstatus)))
            #if os.path.isfile('rebootfail.iku'):
        #os.remove("rebootfail.iku")

    
#error event code
#print the error to the console and inform the user   
@bot.event
async def on_command_error(ctx, error):
    yuyuko = await bot.fetch_user(ownerid)

    if debugmode == True:
        await ctx.send(error)
        return
    
    #command not found
    if isinstance(error, commands.CommandNotFound):
        return

    #if isinstance(error, commands.BotMissingPermissions):
    #    self.missing.perms = 'send_messages'
    #    print('msg_send_fail')
        
    #user has invalid permissions
    if isinstance(error, commands.MissingPermissions):
        #em = discord.Embed(title='Error', description = error, colour=0xc91616)
        #em.set_author(icon_url=bot.user.avatar_url)
        #await ctx.send(embed=em)
        await ctx.send(error)
        return

    if isinstance(error, commands.CommandOnCooldown):
        #em = discord.Embed(title='Error', description = error, colour=0xc91616)
        #em.set_author(icon_url=bot.user.avatar_url)
        #await ctx.send(embed=em)
        #await ctx.send(error)
        await ctx.send("Take it easy! (command on cooldown) Wait %.2fs" % error.retry_after, delete_after=8)
        return
    #user failed check
    if isinstance(error, commands.CheckFailure):
    #note to self: fix this when adding hangout commands       
        #if ctx.author.id != 166189271244472320:
        await ctx.send("Error: Only the owner can use this command")
        return

    #user ran command without an argument         
    if isinstance(error, commands.MissingRequiredArgument):
        #check if the user was using the help command without an arg
        #print (ctx.command.name)
        if ctx.command.name == "help":
            patreons=bot.get_guild(hangoutid).get_role(patreonrole)
            donators = patreons.members
            membernames = [donators.name for donators in donators]
            patreonlist = ", ".join(membernames)
            hlp = open("txt/help.txt", "r")
            help_cmd = hlp.read()
            if patreonlist == "":
                patreonlist = "Nobody :("
                await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
            else:
                await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
            return

        if ctx.command.name == "feed":
            await ctx.send ("Who should i feed?")
            return
            

        else:
            await ctx.send("The " + ctx.command.name + " command requires an argument")
        #em = discord.Embed(title='Error', description = 'a required argument is missing', colour=0xc91616, icon_url=bot.user.avatar_url)
        #await ctx.send(embed=em)
            return

    #Discord API having issues (it always returns a content-type message when it is)
    if str(error) == "Command raised an exception: KeyError: 'content-type'":
        await ctx.send("The Discord API may be having issues at the moment")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Discord API issue)")
            return

    #booru related issue
    #can be intentionally triggered with gif2
    if str(error) == "Command raised an exception: TypeError: 'NoneType' object is not subscriptable":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Got an unusual response from the booru)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Current booru may be down)")
            return

    #booru connection timed out (Gbooru, Port 80)
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:80 ssl:default [Name or service not known]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Timed out trying to connect to Gbooru)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Current booru may be slow down)")
            return

    #booru connection timed out (Gbooru, Port 443)
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:443 ssl:default [Name or service not known]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Timed out trying to connect to Gbooru)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Current booru may be slow down)")
            return

    #Travitia connection failure
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host public-api.travitia.xyz:443 ssl:default [Name or service not known]":
        await ctx.send("Could you try asking me that some other time?")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Cleverbot module may need updating, run =vpsreboot_u)")
            return

    #Image command issue
    if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'group'":
        await ctx.send("There was an issue getting an image, Try that command again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(issue with pixiv id extractor)")
            return

    #Permissions error
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        #try to determine if the user owns/moderates the server or not
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.manage_channels:
            await ctx.author.send("My permissions aren't configured correctly for <#" + str(ctx.message.channel.id) + ">" + "\nPlease check that i have `send messages`, `embed links` and `attach files` permissions for that channel")
            return
        else:        
            await ctx.author.send("It looks like i don't have permission to do that in this channel. \nYour server may have a dedicated bot channel or ask a moderator to fix my permissions for <#" + str(ctx.message.channel.id) + ">")
            return

    #booru connection timed out (Gbooru)
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:80 ssl:default [The semaphore timeout period has expired]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Timed out trying to connect to Gbooru)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Current booru may be slow down)")
            return

    #booru connection broke (Gbooru)
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:80 ssl:default [Temporary failure in name resolution]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Failed to connect to Gbooru)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Gbooru issue?)")
            return

    #Pixiv id extractor broke
    if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'group'":
        await ctx.send("There was an issue getting an image, Try that command again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(issue with pixiv id extractor)")
            return

    #Gelbooru down
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:80 ssl:default [Network is unreachable]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Gelbooru is currently down)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Gbooru issue?)")
            return

    #Gelbooru down/server ca issue
    if str(error) == "Command raised an exception: ClientConnectorError: Cannot connect to host gelbooru.com:443 ssl:default [Network is unreachable]":
        await ctx.send("There seems to be an issue retrieving an image for this command, try again later\n(Gelbooru is either down or there is an internal issue)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Gbooru issue?)")
            return

    #Tweet too long
    if str(error) == "Command raised an exception: TwitterError: Text must be less than or equal to CHARACTER_LIMIT characters.":
        await ctx.send("Your tweet was too long")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content)
            return

    #Y2K22 bug(?)
    if str(error) == "Command raised an exception: TypeError: can't compare offset-naive and offset-aware datetimes":
        await ctx.send("This command is is broken due to a Y2K22 issue, the dev is looking into this")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content)
            return

    #image command not updated yet
    if str(error) == "Command raised an exception: KeyError: 'source'":
        await ctx.send("There was an issue retrieving an image for this command\n(This command hasn't been updated yet)")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(Command needs updating)")
            return

    #Another image command bug
    if str(error) == "Command raised an exception: TypeError: 'NoneType' object is not callable":
        await ctx.send("There was an issue getting an image, Try that command again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(image command bug?)")
            return

    #Yet another image command bug
    if str(error) == "Command raised an exception: ValueError: invalid literal for int() with base 10: ''":
        await ctx.send("There was an issue getting an image, Try that command again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(image command bug?)")
            return

    #generic safebooru
    if 'safebooru' in ctx.message.content:
        await ctx.message.author.send("There was an issue getting an image, Try that again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(image command bug?)")
            return

    #generic gelbooru
    if 'gelbooru' in ctx.message.content:
        await ctx.message.author.send("There was an issue getting an image, Try that again")
        if errordm == True:
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`\n(image command bug?)")
            return
    
    

    #none of the above         
    else:
        #print(error)
        if 'dsay' in ctx.message.content:
            await ctx.message.author.send('Hi, I require `manage messages` permission on this server for dsay to work properly. Ask a server admin to give me this')
            return
        
        #print(str(traceback.print_exc()))
        if errordm == True:
            errormsg = await ctx.send("An error has occured, The dev has been notified")
            #todo: actually put code here that notifies me
            await yuyuko.send("\U000026A0 Error occured: `" + str(error) + "`\nCommand: `" + ctx.message.content + "`")

            #trace = exc.__traceback__            
            #etype = type(exc)
            #lines = traceback.format_exception(etype, exc, trace)
            #traceback_text = ''.join(lines)
            #await ctx.send(traceback_text)
            traceback.print_tb(error.original.__traceback__)
        if errordm == False:
            errormsg = await ctx.send("An error has occured")

#check to see if the user reacts with a peach, if they have then show them detailed error info
        def check(reaction, user):
            return (str(reaction.emoji) == '\U0001f351')
                                   
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
        except asyncio.TimeoutError:
            return
        else:
            if ((reaction.emoji) == '\U0001f351') and reaction.message.id == errormsg.id:
                await ctx.send("Error info: `" + str(error) + "`")
                return


secure_random = random.SystemRandom()
#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content == '<@252442396879486976>':
        await message.channel.send(secure_random.choice(mentioned_nomsg))
        print("[command] mention_nomsg")
        return
    if message.content == '<@!252442396879486976>':
        await message.channel.send(secure_random.choice(mentioned_nomsg))
        print("[command] mention_nomsg")
        return

    if message.content == '<@!252442396879486976>':
        await message.channel.send(secure_random.choice(mentioned_nomsg))
        print("[command] mention_nomsg")
        return

    if message.content == '<@252442396879486976> f':
        await message.channel.send(message.author.name + " has paid their respects")
        print("[command] f")
        return
    if message.content == '<@!252442396879486976> f':
        await message.channel.send(message.author.name + " has paid their respects")
        print("[command] f")
        return

    if message.content == '<@!252442396879486976> f':
        await message.channel.send(message.author.name + " has paid their respects")
        print("[command] f")
        return
    
    #1ccbot commands
    #if message.content == '<@!577823040147161088> spicetools':
        #if message.guild.id != int('162861213309599744'):
            #return
        
        #else:
            #await message.channel.send("Spicetools can be downloaded from " + spiceURL)
            #print("[command] spicetools")
            #return
    
    #= prefix ignoring code (bot list servers)

    #Discord bots
    if message.guild.id == int('110373943822540800') and message.content.startswith('='):
        return
    #Discord bot list
    if message.guild.id == int('264445053596991498') and message.content.startswith('='):
        return
    #= prefix ignoring code (role)
    role = discord.utils.get(message.guild.roles, name="mention_only")
    if role in message.guild.me.roles and message.content.startswith('='):
        #print ('[Debug] = prefix disabled via role')
        return

    #Nitro scam link detection
    #maybe i could try doing this with a txt file like the blacklist files...
    
    #if message.content in scamlinks:
    #if str(scamlinks) in message.content:
        #await message.channel.send("\U000026A0 Known scam URL!")
        #Avoid tenshi also spamming every channel
        #await asyncio.sleep(5)
        #return

    #Nitro scam link detection 2 - Electric Boogaloo
    #i can do this this way but it's clunky af
    
    #if "https://dlscord" in message.content.lower():
        #await message.channel.send("\U000026A0 Scam URL!")
        #return
    
    #https://ostack.cn/?qa=172698/
        

    #enforce english mode 1
    enforce_en1 = discord.utils.get(message.guild.roles, name="tenko_force_en1")
    msg = message.content
    userid = bot.user.id
    if enforce_en1 in message.guild.me.roles:
        

        DetectorFactory.seed = 0
        results = (detect_langs(msg))
        results2 = (detect(msg))
        #print ("[debug] all langs in message: " + str(results))
        #print ("[debug] main lang in message: " + str(results2))
        #print (bot.user.id)

        #check if the user is a mod
        #if message.author.guild_permissions.administrator or message.author.guild_permissions.manage_messages:
            #print ("[debug] user has diplomatic immunity, ignoring")
            #await bot.process_commands(message)
            #return

        #check if user was using a command
        if message.content.startswith('='):
            #print ("[debug] command used, ignoring")
            await bot.process_commands(message)
            return

        if message.content.startswith ('<@!252442396879486976>'):
            #print ("[debug] command used, ignoring")
            await bot.process_commands(message)
            return

        if message.content.startswith ('<@252442396879486976>'):
            #print ("[debug] command used, ignoring")
            await bot.process_commands(message)
            return

        if len(message.content) < 5:
            #print ("[debug] message less than 5 chars, ignoring")
            await bot.process_commands(message)
            return
        
        #check if message has any english at all
        if "en" in str(results):
            #do nothing if english detected
            await bot.process_commands(message)
            return

        if "fr" in str(results2):
            await message.channel.send("Parlez Anglais, s'il vous plaît")
            return

        if "es" in str(results2):
            await message.channel.send("Habla inglés por favor")
            return
        
        if "de" in str(results2):
            await message.channel.send("Englisch sprechen bitte")
            return

        if "ja" in str(results2):
            await message.channel.send("英語でお話ください")
            return
            
            
        else:
            await message.channel.send("Please speak english in this server")
            return


    #enforce english mode 2
    enforce_en2 = discord.utils.get(message.guild.roles, name="tenko_force_en2")
    msg = message.content
    if enforce_en2 in message.guild.me.roles:
        return


    #"sanaed" check
    #check if the user is trying to @ someone (or something) using the sanae command
    
    if message.content.startswith('=sanae <@'):
        #store the message content as a variable an add a blank space to account for people with nicknames
        msg = message.content + ' '
        
        #check if the user is trying to rolemention
        if "<@&" in msg:
            #await message.channel.send("I can't sanae a role")
            #run commands as normal in case someone already uses image commands and role mentions together
            await bot.process_commands(message)

            
        #check if Tenshi has mention only role and do nothing if true
        role = discord.utils.get(message.guild.roles, name="mention_only")
        if role in message.guild.me.roles:
            return

    
        await message.channel.send(msg[7:29] + " has been sanae'd", file=discord.File('pics/sanaed.jpg'))
        print("[command] sanaed")
        return

    if message.content.startswith('<@!252442396879486976>sanae <@'):
        #store the message content as a variable an add a blank space to account for people with nicknames
        msg = message.content + ' '
        
        #check if the user is trying to rolemention
        if "<@&" in msg:
            #await message.channel.send("I can't sanae a role")
            #run commands as normal in case someone already uses image commands and role mentions together
            await bot.process_commands(message)

    
        await message.channel.send(msg[7:29] + " has been sanae'd", file=discord.File('pics/sanaed.jpg'))
        print("[command] sanaed")
        return

    if message.content.startswith('<@252442396879486976>sanae <@'):
        #store the message content as a variable an add a blank space to account for people with nicknames
        msg = message.content + ' '
        
        #check if the user is trying to rolemention
        if "<@&" in msg:
            #await message.channel.send("I can't sanae a role")
            #run commands as normal in case someone already uses image commands and role mentions together
            await bot.process_commands(message)

    
        await message.channel.send(msg[7:29] + " has been sanae'd", file=discord.File('pics/sanaed.jpg'))
        print("[command] sanaed")
        return


#ollama trigger
#check if in TenshiBot Hangout
    role = discord.utils.get(message.guild.roles, name="tenko_skynet")
    if message.guild.id == int('273086604866748426'):# and message.content.startswith('<@!252442396879486976>'):
        print("test")
        await bot.process_commands(message)
        return

    
    
        
    await bot.process_commands(message)

#command logging
@bot.event
async def on_command(ctx):
    print("[command] " + ctx.message.content + " / " + str(ctx.guild))
    #print (ctx.author.display_name)
    return

#    if str(ctx.author.display_name) == 'Yukari' or 'Yukari Yakumo':
#        print ('hi')

#owner check
#19/05 U+1F382
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ownerid
    return commands.check(predicate)

#TenshiBot Hangout check (the name of the Tenshi's server)
#def is_hangout():
#    async def predicate(ctx):
#        return ctx.guild.id == 273086604866748426
#    return commands.check(predicate)

#bot added/kicked from server messages
@bot.event
async def on_guild_join(guild):
        print("[Info] New server get! - " + str(guild))
        payload = {"server_count"  : str(len(bot.guilds))}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url_dbl, data=payload, headers=headers_dbl)
        
@bot.event
async def on_guild_remove(guild):
        print("[Info] Kicked from a server - " + str(guild))
        payload = {"server_count"  : str(len(bot.guilds))}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url_dbl, data=payload, headers=headers_dbl)
    
#help command
@bot.command()
async def help(ctx, *, eirin):
    #help me eirin!
    #print (eirin)
    if eirin.lower() == "me eirin":
        #await ctx.send("a")
        patreons=bot.get_guild(hangoutid).get_role(patreonrole)
        donators = patreons.members
        membernames = [donators.name for donators in donators]
        patreonlist = ", ".join(membernames)
        hlp = open("txt/help.txt", "r")
        help_cmd = hlp.read()
        if patreonlist == "":
            patreonlist = "Nobody :("
            await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
        else:
            await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
        return
    
    else:
        patreons=bot.get_guild(hangoutid).get_role(patreonrole)
        donators = patreons.members
        membernames = [donators.name for donators in donators]
        patreonlist = ", ".join(membernames)
        hlp = open("txt/help.txt", "r")
        help_cmd = hlp.read()
        if patreonlist == "":
            patreonlist = "Nobody :("
            await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
        else:
            await ctx.send(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
        return

@bot.command()
async def help2(ctx):
    em = discord.Embed(title='TenshiBot Help', description='Desc', colour=0x42D4F4)
    em.set_author(name='Author')
    #em.set_image(url=booruappend + msg)
    em.add_field(name="General Commands", value=gen_command, inline=False)
    em.add_field(name="Fun Commands", value=fun_command, inline=False)
    em.add_field(name="Image Commands", value=img_command, inline=False)
    em.set_footer(text="Version " + bot_version + " ,Created by KawashiroDev")
    await ctx.send(embed=em)

@bot.command()
@is_owner()
async def getpatreons(ctx):
    patreons=bot.get_guild(hangoutid).get_role(patreonrole)
    print(patreons)
    donators = patreons.members
    membernames = [donators.name for donators in donators]
    print(membernames)
    patreonlist = ", ".join(membernames)
    await ctx.send(patreonlist)

@bot.command()
async def showpatreons(ctx):
    patreons=bot.get_guild(hangoutid).get_role(patreonrole)
    print(patreons)
    donators = patreons.members
    membernames = [donators.name for donators in donators]
    print(membernames)
    patreonlist = ", ".join(membernames)
    await ctx.send("TenshiBot Patreons: " + patreonlist)

#@bot.command()
#@commands.cooldown(1, 20, commands.BucketType.user)
#async def isnowillegal(ctx, legal : str):
#    """Make Stuff Illegal!"""
#    legal = legal.upper()
#    url = "https://storage.googleapis.com/is-now-illegal.appspot.com/gifs/" + legal +".gif"
#    em = discord.Embed(title="{} is now Illegal!".format(legal))
#    em.set_image(url=url)
#    await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def feed(ctx, user : discord.Member):
    if user == None:
        await ctx.send(f" {ctx.message.author.mention} eats {random.choice(food)} ")
        return
    if user == ctx.message.author:
        await ctx.send(f" {ctx.message.author.mention} eats {random.choice(food)} ")
        return
    else:
        await ctx.send(f"** Hands {user.name} a {random.choice(food)} **")
        return

#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')
#    await bot.send_typing(channel)

@bot.command()
@is_owner()
async def githubtest(ctx):
    repo = g.get_repo("KawashiroDev/TenshiBot")
    branch = repo.get_branch("master")
    #get the sha of latest commit
    print(branch.commit.sha)
    latestsha = branch.commit.sha
    commit = repo.get_commit(sha=latestsha)
    print(commit.commit.author.date)
    #repo = g.get_repo("99710/TenshiBot")
    #print(commit.commit.author.date)
    #print(repo.name)
    #print(dir(branch.commit))

@bot.command()
@is_owner()
async def update(ctx):
    print('[Updater] Getting info from github')
    repo = g.get_repo("KawashiroDev/TenshiBot")
    branch = repo.get_branch("master")
    #get the sha of latest commit
    print(branch.commit.sha)
    latestsha = branch.commit.sha
    #get UTC commit time from sha
    commit = repo.get_commit(sha=latestsha)
    latest_commit = commit.commit.author.date
    #dump to console for testing
    print("githubtime")
    print(latest_commit)
    print("dirtime")
    #get latest file
    list_of_files = glob.glob('/Users/99710/Documents/GitHub/TenshiBot/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    #dump latest file name to console
    print (latest_file)
    #get time of latest file and dump to console
    newest_file = os.path.getmtime(latest_file)
    print(newest_file)
    #convert unix time to utc and remove miliseconds
    utc_folder = datetime.fromtimestamp(newest_file, tz=timezone.utc).replace(microsecond=0, tzinfo=None)
    #dump to console
    print (utc_folder)
    if latest_commit > utc_folder:
        print ('[Updater] Github is newer than current build, starting update process')
        await ctx.send('Github is newer than local, preparing to update')
        #async with aiohttp.ClientSession() as session:
        #    async with session.get('https://github.com/kawashirodev/TenshiBot/archive/master.zip') as resp:
        #        await resp.read()
        #    with open('update.zip', 'wb') as fd:
        #        while True:
        #            chunk = await resp.read()
        #    if not chunk:
        #        return
        #    fd.write(chunk)
        
        #above doesn't work, adapting spicetools extraction code from 1ccbot instead
        #yes requests is bad but eh
        
        spiceURL = 'https://github.com/kawashirodev/TenshiBot/archive/master.zip'
        r = requests.get(spiceURL)
        with open('Tenshiupdate.zip', 'wb') as f:
            f.write(r.content)

            zf = ZipFile('Tenshiupdate.zip', 'r')
            #extract spicetools archive
            zf.extractall('Tenshiupdate')
            zf.close()
            #define dirs
            update_dir = 'Tenshiupdate/TenshiBot-master'
            target_dir = 'test'
            #get all files in update folder
            files_list = os.listdir(update_dir)
            print(files_list)
            for files in files_list:
                shutil.copytree(update_dir, target_dir)

            #delete files
            #shutil.rmtree("spice_extracted")
            #os.remove("Spicetools_src.zip")
        
    else:
        print ('[Updater] Current version newer than Github, aborting update')
        await ctx.send('Local is newer than Github, aborting')
        return
    
    #print (time.ctime(max(os.path.getmtime(root) for root,_,_ in os.walk('/TenshiBot'))))
    #repo = g.get_repo("kawashirodev/TenshiBot")
    #print(commit.commit.author.date)
    #print(repo.name)
    #print(dir(branch.commit))

#@bot.command()
#@is_owner()
#async def eval(ctx, *, code):
#    str_obj = io.StringIO() #Retrieves a stream of data
#    try:
#        with contextlib.redirect_stdout(str_obj):
#            exec(code)
#    except Exception as e:
#        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
#    await ctx.send(f'```{str_obj.getvalue()}```')

@bot.command()
@is_owner()
async def ldtest(ctx, *, args):
    DetectorFactory.seed = 0
    await ctx.send(detect_langs(args))
    print (detect_langs(args))

@bot.command()
async def dmtest(ctx):
    yuyuko = bot.get_user(166189271244472320)
    await yuyuko.send("Yo!")
    return

@bot.command()
async def kofi(ctx):
    await ctx.send('https://ko-fi.com/h99710')

@bot.command()
@is_owner()
async def playsound(ctx):
    playsound('Entry_3DX+.mp3', False)
    print ("[Debug] Playing sound file")

@bot.command()
@commands.cooldown(1, 90, commands.BucketType.default)
async def techno(ctx):
    await ctx.send("***TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send("*** TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send("***  TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send(">Don't touch the keyboard<")
    await asyncio.sleep(0.9)
    await ctx.send("***   TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send("***    TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send("***     TECHNO TECHNO TECHNO***")
    await asyncio.sleep(0.9)
    await ctx.send(file=discord.File('pics/techno.png'))

@bot.command()
@is_owner()
async def content_test(ctx):
    #get last 50 messages in channel
    history = (await ctx.guild.get_channel(ctx.channel.id).history(limit=10).flatten())
    #messages = await ctx.channel.fetch_message(limit=5).flatten()
    messages = await ctx.channel.history.content(limit=5).flatten()
    lastmessage = await ctx.channel.fetch_message(ctx.channel.last_message_id)
    print (messages)
    return
    #check if
    #if str(message.guild.me.id) in str(history):


@bot.command()
@is_owner()
async def tenshichat(ctx, *, prompt: str):
    print("[Debug] AI prompt = " + prompt)
    
    #trigger typing state
    async with ctx.typing():

        full_response = ""
        typing_task = None

    async with aiohttp.ClientSession() as session:
        async with session.post(ollamaurl, json={"model": chatmodel, "prompt": prompt}) as response:
            print("[Debug] Posted prompt to server")

            async def keep_typing():
                while True:
                    async with ctx.typing():
                        await asyncio.sleep(5)
                        print("[Debug] Typing task running")

            typing_task = asyncio.create_task(keep_typing())
            print("[Debug] Started typing task")

            async for line in response.content:
                line_text = line.decode("utf-8").strip()
                print("[Debug] Raw response = " + line_text)
                
                try:
                    data = json.loads(line_text)
                    if "response" in data:
                        full_response += data["response"]
                except json.JSONDecodeError:
                    print("[Debug] JSON error on line:", line_text)


            typing_task.cancel()
            print("[Debug] Stopped typing task")
    if full_response:
        print("[Debug] Full response = " + full_response)
        await ctx.send(full_response[:2000])
    else:
        await ctx.send("Failed")
        return

@bot.command()
async def honk(ctx):
    await ctx.send(file=discord.File("pics/honk/" + random.choice(os.listdir("pics/honk"))))

@bot.command()
async def fumo_local(ctx):
    if limit_net == True:
        await ctx.send('fumo')
        return
    await ctx.send(file=discord.File("pics/fumo/" + random.choice(os.listdir("pics/fumo"))))

@bot.command()
async def dumpserverid(ctx):
    await ctx.send(ctx.guild.id)

@bot.command()
async def nestedreacttest(ctx):
    L1 = await ctx.send('Level 1')

    def check(reaction, user):
        return (str(reaction.emoji) == '\U0001f351') or (str(reaction.emoji) == '\U0001f352')
                                   
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Timeout')
        return
    else:
        if ((reaction.emoji) == '\U0001f351') and reaction.message.id == L1.id:
            L2 = await ctx.send('Level 2')

            def check(reaction, user):
                return (str(reaction.emoji) == '\U0001f351')
                                   
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Timeout')
                return
            else:
                if ((reaction.emoji) == '\U0001f351') and reaction.message.id == L2.id:
                    await ctx.send('Success')
        #cherry                
        if ((reaction.emoji) == '\U0001f352') and reaction.message.id == L1.id:                 
            L2a = await ctx.send('Level 2 alternate')
            def check(reaction, user):
                return (str(reaction.emoji) == '\U0001f351')
                                   
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send('Timeout')
                return
            else:
                if ((reaction.emoji) == '\U0001f351') and reaction.message.id == L2a.id:
                    await ctx.send('Success alternate')
    

@bot.command()
async def typingtest(ctx):
    await ctx.send('pong')
    await bot.send_typing(channel)    
    

#nsfw flag check
@bot.command()
async def nsfwtest(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send('nsfw')
    else:
        await ctx.send('not nsfw')


@commands.has_permissions(administrator=True)
@bot.command()
async def permstest(ctx):
    await ctx.send('ok')

#@commands.slash_command()  # create a slash command for the supplied guilds
#async def hello(ctx):
#    await ctx.respond(f"Hello {ctx.author}!")

@bot.command()
@is_owner()
async def ping2(ctx):
    await ctx.respond('pong')

@bot.command()
async def errortest(ctx):
    await()

past = datetime.now() - timedelta(days=9999)

#@bot.command()
#async def accdatetest(ctx):
#    yuyuko = bot.get_user(166189271244472320)
#    await ctx.send("Yuyuko created at " + str(yuyuko.created_at))
#    await ctx.send(str(past))
    #if account creation date is newer than specified date
#    if yuyuko.created_at > past:
#        await ctx.send("fail")
#        return
#    else:
#        await ctx.send("pass")
#        return

@bot.command()
async def restart(ctx):
    if ctx.author.id != ownerid:
        return
    else:
        await ctx.send("Restarting...")
        os.system("chmod +x reboot.sh")        
        os.system("./reboot.sh")
        return

@bot.command()
async def accdatetest2(ctx):
    await ctx.send("author created at " + str(ctx.author.created_at))
    await ctx.send(str(past))
    #if account creation date is newer than specified date
    if ctx.author.created_at > past:
        await ctx.send("fail")
        return
    else:
        await ctx.send("pass")
        return    

#basic admin functionality
@bot.command()
@is_owner()    
async def vpsreboot(ctx):
    await bot.change_presence(activity=discord.Game(name="Rebooting..."))
    if smartboot == True:
        await ctx.send('Creating reboot file')
        reboot = open("reboot.tenko", "w")
        reboot.close()
        #sys.stdout.close()
        await ctx.send('Rebooting the VPS')
        os.system("sudo reboot")
    else:
        await ctx.send('Rebooting the VPS')
        #sys.stdout.close()
        os.system("sudo reboot")
    #os.system("shutdown -r -t 30")

@bot.command()
@is_owner()
async def update_pycord(ctx):
    await ctx.send("Updating pycord and restarting")
    #does it even work like this?
    #will KawashiroDev stop writing these random comments?
    #tune into whenever 99710 next uploads a video to find out!

    #go into the update folder
    os.system("cd Update")
    #make file executeable because "what is security"
    os.system("chmod +x pycord_update.sh")
    #execute script
    os.system("./pycord_update.sh")
    return

#todo: fix this
@bot.command()
@is_owner()
async def vpsreboot_u(ctx):
    await bot.change_presence(activity=discord.Game(name="Updating..."))
    await ctx.send('Updating...')
    os.system("python3.7 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U")
    await bot.change_presence(activity=discord.Game(name="Rebooting..."))
    await ctx.send('Updates complete, Restarting server')
    os.system("sudo reboot")


#status changing command
@bot.command()
@is_owner()  
async def setstatus_stream(ctx, *, args):
    await bot.change_presence(activity=discord.Streaming(name= args, url='https://twitch.tv/saigyouji8'))

@bot.command()
@is_owner()  
async def setstatus(ctx, *, args):
    await bot.change_presence(activity=discord.Game(name= args))
    await ctx.send("status set to " + "`" + args + "`")

#command doesn't work on a verified bot
#rip CirnoBot/OkuuBot 2016-2019(i think)
@bot.command()
@is_owner()  
async def setname(ctx, *, args):
    await bot.user.edit(username= args)

@bot.command()
@is_owner()  
async def setnick(ctx, *, args):
    await ctx.guild.me.edit(nick = args)
    await ctx.send("nickname set to " + "`" + args + "`")

#has to point to a png file
@bot.command()
@is_owner()
#async def setavatar(ctx, *, args):
async def setavatar(ctx):
    #image = args   
    image = "C:/Users/H99710/Pictures/TenshiBot_avatar.png"
    newavatar = open(image, 'rb')
    await bot.user.edit(avatar = newavatar.read() )

@bot.command()
@is_owner()
async def shuffleavatar(ctx):   
#    image = (secure_random.choice(shuffle_test))
    image =  "avatars/normal/" + random.choice(os.listdir("avatars/normal"))
    newavatar = open(image, 'rb')
    await bot.user.edit(avatar = newavatar.read())
    await ctx.send("Avatar shuffled!")

     
@bot.command()
@is_owner()
async def cirnomode(ctx):   
    image = "avatars/alt_char/cirno/" + random.choice(os.listdir("avatars/alt_char/cirno"))
    newavatar = open(image, 'rb')
    #await bot.user.edit(username="CirnoBot", avatar = newavatar.read())
    await bot.user.edit(avatar = newavatar.read())
    await bot.change_presence(activity=discord.Game(name="Happy Cirno Day!"))
    await ctx.send("Enabled Cirnomode, Reset to Tenshi with `tenkomode`")
  
@bot.command()
@is_owner()
async def tenkomode(ctx):   
    image =  "avatars/normal/" + random.choice(os.listdir("avatars/normal"))
    newavatar = open(image, 'rb')
    #await bot.user.edit(username="TenshiBot", avatar = newavatar.read())
    await bot.user.edit(avatar = newavatar.read())
    await bot.change_presence(activity=discord.Game(name="with Iku"))
    await ctx.send("Enabled Tenshimode")    

#ban test command
@bot.command()
@is_owner()
async def bantest(ctx):
    await ctx.author.ban(reason=':)')
    await ctx.author.unban

#kick test command
@bot.command()
@is_owner()
async def kickme(ctx):
    await ctx.author.kick(reason='.')

#server leaving command
@bot.command()
@is_owner()
async def yeetserver(ctx, serverid):
    youmu = bot.get_guild(int(serverid))
    print (youmu)
    await youmu.leave()
    #await ctx.send("yeeted from " + youmu.name())

@bot.command()
@is_owner()
async def delmsg(ctx, arg):
    msg = bot.get_message(int(arg))
    await msg.delete()
    await ctx.send("message deleted")

#console command
@bot.command()
@is_owner()
#freezes the bot!
async def console(ctx):
    cmd=ctx.message.content[len("<@571094749537239042> console"):].strip()
    result = subprocess.check_output([cmd], stderr=subprocess.STDOUT)
    #os.system(ctx.message.content)
    await ctx.send(result)

    

@bot.command()
async def about(ctx):
    second = time.time() - st
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    uptime='%dw,' % (week) + ' %dd,' % (day) + ' %dh,' % (hour) + ' %dm,' % (minute) + ' and %ds.' % (second)
    servercount=str(len(bot.guilds))
    buildinfo="%s" % time.ctime(os.path.getmtime("Tenshi.py"))
    pycordver=(discord.__version__)
    

    em=discord.Embed(colour=0x00ffff)
    em.set_author(name= bot.user.name + ' info')#, icon_url=bot.user.avatar_url)
    em.add_field(name="Version", value=bot_version, inline=True)
    em.add_field(name="Servercount", value=servercount, inline=True)
    em.add_field(name="Uptime", value=uptime, inline=False)
    em.add_field(name="Tenshi.py timestamp", value=buildinfo, inline=False)
    em.add_field(name="Pycord version", value=pycordver, inline=False)
    em.set_footer(text="Created by KawashiroDev")
    await ctx.send(embed=em)

@bot.command()
async def about_adv(ctx):    
    await ctx.send('``` [about2] \n```')

@bot.command()
async def invite(ctx):
    await ctx.send('Use this link to add me to your server: <https://discordapp.com/oauth2/authorize?client_id=252442396879486976&scope=bot&permissions=67161152>')
#    if botid == none:
#        await ctx.send('Use this link to add me to your server: <https://discordapp.com/oauth2/authorize?client_id=252442396879486976&scope=bot&permissions=67161152>')
#    else:
#        await ctx.send('Use this link to add <@' + botid +  '> to your server: <https://discordapp.com/oauth2/authorize?client_id=' + botid + '&scope=bot&permissions=67161152>')

@bot.command()
async def support(ctx):
    await ctx.send('Need help with something or just want to chat with other users? Join TenshiBot Hangout: https://discord.gg/vAbzRG9')

@bot.command()
async def rate(ctx):
    await ctx.send("I rate it " + str(randint(0,10)) + "/10")

@bot.command()
async def md(ctx, arg):
    await ctx.send("`" + arg + "`")

@bot.command()
async def emote(ctx, arg):
    await ctx.send("<" + arg + ">")

@bot.command()
async def say(ctx, *, args):
    if "@everyone" in args:
        await ctx.send("`" + args + "`")
        return
    if "@here" in args:
        await ctx.send("`" + args + "`")
        return
    else:
        await ctx.send(args)
        return

@bot.command()
async def dsay(ctx, *, args):
    if "@everyone" in args:
        await ctx.send("`" + args + "`")
        await ctx.message.delete()
        return
    if "@here" in args:
        await ctx.send("`" + args + "`")
        await ctx.message.delete()
        return
    else:
        await ctx.send(args)    
        await ctx.message.delete()
        return

#@bot.command()
#@is_owner()
#async def ttstest(ctx, *, args):
    #await speak(args, "en", save=True, file="voice.mp3", speak=False)
    #return

@bot.command()
async def patreon(ctx):
    await ctx.send('Want to support TenshiBot on patreon? \nPatreon donators get featued in the help command as well as a donator role in the TenshiBot Hangout Discord\nhttp://patreon.com/tenshibot')    


@bot.command()
async def jojo(ctx, arg):
    if "@everyone" in arg:
        await ctx.send("`" + arg + "`" + ' has been stopped!', file=discord.File('pics/stop.jpg'))
        return
    if "@here" in arg:
        await ctx.send("`" + arg + "`" + ' has been stopped!', file=discord.File('pics/stop.jpg'))
        return
    else:    
        await ctx.send(arg + ' has been stopped!', file=discord.File('pics/stop.jpg'))
        return
    
@bot.command()
async def banana(ctx, arg):
    if "@everyone" in arg:
        await ctx.send("`" + arg + "`" + ' has been banaed!', file=discord.File('pics/banana.png'))
        return
    if "@here" in arg:
        await ctx.send("`" + arg + "`" + ' has been banaed!', file=discord.File('pics/banana.png'))
        return
    else:    
        await ctx.send(arg + ' has been banaed!', file=discord.File('pics/banana.png'))
        return

@bot.command()
async def cirnoed(ctx, arg):
    if "@everyone" in arg:
        await ctx.send("`" + arg + "`" + ' has been cirnoed!', file=discord.File('pics/cirnoed.jpg'))
        return
    if "@here" in arg:
        await ctx.send("`" + arg + "`" + ' has been cirnoed!', file=discord.File('pics/cirnoed.jpg'))
        return
    else:    
        await ctx.send(arg + ' has been cirnoed!', file=discord.File('pics/cirnoed.jpg'))
        return

@bot.command()
async def oil(ctx, arg):
    if "@everyone" in arg:
        await ctx.send("`" + arg + "`" + ' has been oiled!', file=discord.File('pics/oil.png'))
        return
    if "@here" in arg:
        await ctx.send("`" + arg + "`" + ' has been oiled!', file=discord.File('pics/oil.png'))
        return
    else:    
        await ctx.send(arg + ' has been oiled!', file=discord.File('pics/oil.png'))
        return    

@bot.command()
async def confused(ctx):
    await ctx.send(file=discord.File('pics/confused.jpg'))

@bot.command()
async def hooray(ctx):
    await ctx.send(file=discord.File('pics/hooray.png'))    

@bot.command()
async def thonk(ctx):
    await ctx.send(file=discord.File('pics/thonk.gif'))

@bot.command()
async def touhover(ctx):
    await ctx.send(file=discord.File('pics/touhover.png'))


#ai stuff
#the issue with ai stuff is i can't find a good async cb.io module to use
#ai commands take a few seconds to respond which freezes the bot

#for now i'm just going leave ai disabled    
cb_user = ''
cb_key = ''
cb_nick = 'Tenko_AI'

@bot.command()
@is_owner()
async def tenko_ai(ctx, *, args):
    ai2 = cleverbot_io.set(user= cb_user , key= cb_key , nick= cb_nick )
    #this cleverbot engine has a delay so send a typing status to look like something is happening
    #await client.send_typing(channel)
    #answer = (ai2.ask(ctx.message.content[len("<@571094749537239042> ai"):].strip()))
    answer = ai2.ask(args)
    #await client.send_typing(channel)
    await ctx.send(answer)


#alternate cleverbot.io interface module
#this one has an async option but i can't get it to work as async
#https://pypi.org/project/cleverbotio/
@bot.command()
@is_owner()
async def tenko_ai2(ctx, *, args):    

    cb = Cleverbotio.Cleverbot(cb_user, cb_key, cb_nick)
    cb.create_session()
    answer2 = cb.say(args)
    await ctx.send(answer2)

#Slash commands

@bot.slash_command(name="test", description="Test command")
async def testcommand(ctx):
    await ctx.respond('Thats not it')

#@bot.slash_command(name="test2", description="Test command")
#async def testcommand2(ctx):
    #await ctx.send('Thats not it')

@bot.slash_command(name="about", description="View Tenshi info")
async def about_slash(ctx):
    second = time.time() - st
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    uptime='%dw,' % (week) + ' %dd,' % (day) + ' %dh,' % (hour) + ' %dm,' % (minute) + ' and %ds.' % (second)
    servercount=str(len(bot.guilds))
    buildinfo="%s" % time.ctime(os.path.getmtime("Tenshi.py"))
    pycordver=(discord.__version__)

    em=discord.Embed(colour=0x00ffff)
    em.set_author(name= bot.user.name + ' info')#, icon_url=bot.user.avatar_url)
    em.add_field(name="Version", value=bot_version, inline=True)
    em.add_field(name="Servercount", value=servercount, inline=True)
    em.add_field(name="Uptime", value=uptime, inline=False)
    em.add_field(name="Tenshi.py timestamp", value=buildinfo, inline=False)
    em.add_field(name="Pycord version", value=pycordver, inline=False)
    em.set_footer(text="Created by KawashiroDev")
    await ctx.respond(embed=em)


@bot.slash_command(name="support", description="Invite link for Tenshi's server")
async def support_slash(ctx):
    await ctx.respond('Need help with something or just want to chat with other users? Join TenshiBot Hangout: https://discord.gg/vAbzRG9')


@bot.slash_command(name="honk", description="Send a random Chen honk image")
async def honk_slash(ctx):
    await ctx.respond(file=discord.File("pics/honk/" + random.choice(os.listdir("pics/honk"))))

@bot.slash_command(name="help", description="Command information")
async def help_slash(ctx):
    patreons=bot.get_guild(hangoutid).get_role(patreonrole)
    donators = patreons.members
    membernames = [donators.name for donators in donators]
    patreonlist = ", ".join(membernames)
    hlp = open("txt/help.txt", "r")
    help_cmd = hlp.read()
    if patreonlist == "":
        patreonlist = "Nobody :("
        await ctx.respond(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
    else:
        await ctx.respond(help_cmd + "**Patreon Supporters** ```" + patreonlist + " ```")
    return

@bot.slash_command(name="patreon", description="Patreon link")
async def patreon_slash(ctx):
    await ctx.respond('Want to support TenshiBot on patreon? \nPatreon donators get featued in the help command as well as a donator role in the TenshiBot Hangout Discord\nhttp://patreon.com/tenshibot')

#this has to be at the end of the code
#client.run(token)
if debugmode == True:
    tkn = open("Tokens/tenshi_debug.txt", "r")
else:
    tkn = open("Tokens/tenshi_production.txt", "r")
token = tkn.read()
tkn.close()    
#bot.run(token, bot=True, reconnect=True)
bot.run(token, reconnect=True)
