#TenshiBot Slipstream version
#Created by KawashiroDev


##Parameters##

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '2.4.9'

#Owner ID
ownerid = 166189271244472320

#hangout ID
hangoutid = 273086604866748426

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
ghost = True

#Sound on boot (debug only)
bootsound = True

#windows check
#if this directory exists then run in debug mode
#if not then run in production mode
win_dir_check = '/windows'

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
import twitter
import datetime
import playsound
import async_cleverbot as ac
import sys
import glob
import zipfile
import shutil
import hashlib
import contextlib
import io
import logging

from discord.ext import commands
from random import randint
from bs4 import BeautifulSoup
from urlextract import URLExtract
#from Cleverbotio import 'async' as cleverbot
#from saucenaopy import SauceNAO
from datetime import datetime, timedelta, timezone
from playsound import playsound
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory
from github import Github
from zipfile import ZipFile

#https://www.microsoft.com/en-us/download/details.aspx?id=48159
from profanityfilter import ProfanityFilter

print('[Startup] Please wait warmly...')

#start logging console
#sys.stdout = open("test.txt", "w")
#print('test')


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#define intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.AutoShardedBot(command_prefix=('=='), case_insensitive=True, shard_count=3, intents=intents)
    
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
bot.remove_command("help")




@bot.event
async def on_ready():
    yuyuko = await bot.fetch_user(ownerid)
    #print(yuyuko)

    await yuyuko.send("System ready!")
        
    print('TenshiBot startup complete ')
    print('User ID - ' + str(bot.user.id))
    print('Username - ' + bot.user.name)
    print('Shard Count - ' + str(bot.shard_count))
    print('TenshiBot Ver - ' + bot_version)
    print('System Variant - ' + bot_variant)
    print(' ')
    print('servercount - ' + str(len(bot.guilds)))
    print(discord.version_info)

    
#error event code
#print the error to the console and inform the user   
@bot.event
async def on_command_error(ctx, error):
    yuyuko = await bot.fetch_user(ownerid)
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
        if ctx.author.id != 166189271244472320:
            await ctx.send("Error: Only the owner can use this command")
            return
            
        else:
            await ctx.send("Error: This command can only be used in TenshiBot Hangout")#

    #user ran command without an argument         
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: This command requires an argument")
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

    #Permissions error
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        #try to determine if the user owns/moderates the server or not
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.manage_channels:
            await ctx.author.send("My permissions aren't configured correctly for <#" + str(ctx.message.channel.id) + ">" + "\nPlease check that i have `send messages`, `embed links` and `attach files` permissions for that channel")
            return
        else:        
            await ctx.author.send("It looks like i don't have permission to do that in this channel. \nYour server may have a dedicated bot channel or ask a moderator to fix my permissions for <#" + str(ctx.message.channel.id) + ">")
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
    await bot.process_commands(message)

#owner check
#19/05 U+1F382
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == ownerid
    return commands.check(predicate)

#help command
@bot.command()
async def help(ctx):
    hlp = open("txt/help.txt", "r")
    help_cmd = hlp.read()
    await ctx.send(help_cmd)


@bot.command()
async def test(ctx):
    await ctx.send('pong')

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
    em.add_field(name="Tenshi.py timestamp", value=buildinfo, inline=False)
    em.set_footer(text="Created by KawashiroDev")
    await ctx.send(embed=em)



tkn = open("Tokens/tenshi_production.txt", "r")
token = tkn.read()
tkn.close()    
bot.run(token, bot=True, reconnect=True)
