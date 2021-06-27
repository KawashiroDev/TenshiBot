#IkuBot (Tenshi watchdog)
#Created by KawashiroDev


##Parameters##

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.0.0'

#Owner ID
ownerid = 166189271244472320

#hangout ID
hangoutid = 273086604866748426

#Patreon role ID
patreonrole = 367069832405057546

#YT membership role ID
yt_member = 454051781371232291

#TenshiBot ID
tenkoid = 252442396879486976

#Debug TenshiBot ID
debugtenkoid = 454051781371232291

#TenshiBot link mode (future use)
#Serverside - Check if Tenshi is running by listening on a port
#Console - Check if Tenshi is running using pgrep
#Discord - Check if Tenshi is online by querying the Discord API
#None 
tenkolink = None

#Limited network mode
#enable to reduce Tenshi's data usage if running on slow wifi or 3g/4g
limit_net = False

#DM on boot (production only)
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

import discord
#import requests
import aiohttp
import random
import asyncio
import os
import subprocess
import time
import traceback
import lxml
import datetime
import sys
import glob
import zipfile
import shutil
import contextlib
import io
import logging
import setproctitle
import psutil

from discord.ext import commands
from random import randint
from datetime import datetime, timedelta, timezone
from github import Github

#https://www.microsoft.com/en-us/download/details.aspx?id=48159
from profanityfilter import ProfanityFilter

print('[Startup] Please wait warmly...')

#change process title
setproctitle.setproctitle('Iku ')

#start logging console
#sys.stdout = open("test.txt", "w")
#print('test')


#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)


print('[Startup] Starting Iku')
bot_mode = 'Production'
debugmode = False

mentioned_nomsg = [
"Hm..",
]

playingstatus = [
"with Tenshi",
]

#define intents

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
 
bot = commands.Bot(command_prefix=commands.when_mentioned, case_insensitive=True, intents=intents)
    
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
#bot.remove_command("help")

#Sharding! should help with performance since the bot is on 1000+ servers
#client = discord.AutoShardedClient()
#client = discord.Client()

st = time.time()

git = open("Tokens/github.txt", "r")
git_token = git.read()
g = Github(git_token)

async def Tenshi_autorestart():
    await bot.wait_until_ready()
    tenshi = bot.get_guild(hangoutid).get_member(tenkoid)
    while True:
        await asyncio.sleep(600)
        print (tenshi.status)
        #check if Tenshi is offline
        if str(tenshi.status) == "online":
            #and a reboot already hasn't been tried
            if os.path.isfile('reboottried.iku'):
                print ("[Debug] Already tried a reboot, ignoring")
                #return
            else:
                print ("[Debug] Tenshi offline!")
                #run Tenshi's reboot script and wait
                os.system("chmod +x reboot.sh")        
                os.system("./reboot.sh")
                await asyncio.sleep(30)
                #check if tenshi is still offline
                if str(tenshi.status) == "offline" :
                    #give up
                    reboot = open("rebootfail.iku", "w")
                    reboot.close()
                
            



@bot.event
async def on_ready():
    yuyuko = await bot.fetch_user(ownerid)
    tenshi = await bot.fetch_user(tenkoid)
    #print(yuyuko)

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

    await bot.change_presence(activity=discord.Game(name="IKU [" + bot_version + "]"))
    await asyncio.sleep(5)
    #await bot.change_presence(activity=discord.Game(name="Startup complete"))
    #await asyncio.sleep(5)
    #await bot.change_presence(activity=discord.Streaming(name="TenshiBot", url='https://twitch.tv/99710'))
    await bot.change_presence(activity=discord.Game(name=random.choice(playingstatus)))

    
#error event code
#print the error to the console and inform the user   
@bot.event
async def on_command_error(ctx, error):
    await ctx.send("An error has occured: " + str(error))


secure_random = random.SystemRandom()
#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    #if message.author == bot.user:
    #    return
    #if message.author.bot:
    #    return

    #if message.content == '<@252442396879486976>':
        #await message.channel.send(secure_random.choice(mentioned_nomsg))
        #print("[command] mention_nomsg")
        #return
    #if message.content == '<@!252442396879486976>':
        #await message.channel.send(secure_random.choice(mentioned_nomsg))
        #print("[command] mention_nomsg")
        #return

    #if message.content == '<@!252442396879486976>':
        #await message.channel.send(secure_random.choice(mentioned_nomsg))
        #print("[command] mention_nomsg")
        #return
    
    await bot.process_commands(message)

#command logging
@bot.event
async def on_command(ctx):
    print("[command] " + ctx.message.content + " / " + str(ctx.guild))
    return


#owner check
#19/05 U+1F382
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ownerid
    return commands.check(predicate)

#help command
#@bot.command()
#async def help(ctx):
#    hlp = open("txt/help_iku.txt", "r")
#    help_cmd = hlp.read()
#    await ctx.send(help_cmd)

@bot.command()
@is_owner()
async def getpatreons(ctx):
    patreons=bot.get_guild(hangoutid).get_role(patreonrole)
    print(patreons)
    donators = patreons.members
    membernames = [donators.name for donators in donators]
    print(membernames)
    patreonlist = "\n".join(membernames)
    await ctx.send(patreonlist)

@bot.command()
@is_owner()
async def gettenshi(ctx):
    tenshi = await bot.fetch_user(tenkoid)
    tenshi2 = bot.get_guild(hangoutid).get_member(tenkoid)
    print (tenshi2.status)
    await ctx.send(tenshi2.status)

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
async def vpsreboot_u(ctx):
    await bot.change_presence(activity=discord.Game(name="Updating..."))
    await ctx.send('Updating...')
    os.system("python3.5 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U")
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
async def about(ctx):
    second = time.time() - st
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    uptime='%dw,' % (week) + ' %dd,' % (day) + ' %dh,' % (hour) + ' %dm,' % (minute) + ' and %ds.' % (second)
    servercount=str(len(bot.guilds))
    buildinfo="%s" % time.ctime(os.path.getmtime("Tenshi.py"))

    em=discord.Embed(colour=0x00ffff)
    em.set_author(name= bot.user.name + ' info', icon_url=bot.user.avatar_url)
    em.add_field(name="Version", value=bot_version, inline=True)
    em.add_field(name="Servercount", value=servercount, inline=True)
    em.add_field(name="Uptime", value=uptime, inline=False)
    em.add_field(name="Iku.py timestamp", value=buildinfo, inline=False)
    em.set_footer(text="Created by KawashiroDev")
    await ctx.send(embed=em)

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


#this has to be at the end of the code
#client.run(token)
tkn = open("Tokens/iku.txt", "r")
token = tkn.read()
tkn.close()

bot.loop.create_task(Tenshi_autorestart())
#bot.loop.create_task(getpatreons())
#bot.loop.create_task(Tenshi_update())
#bot.loop.create_task(Server_update())

bot.run(token, bot=True, reconnect=True)
