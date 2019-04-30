#TenshiBot Slipstream version
#Created by 99710

#this version is still in early development and NOT ready to replace the main version

#todo
#server count display and posting
#dev id checking for some commands


##Parameters##

#Discordbots.org API key
dbo_api = ''

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.5'

#Booting text
print('Please wait warmly...')

#owner id

import discord
import requests
import aiohttp
import praw
import lxml
import random
import asyncio
import os
import subprocess

from discord.ext import commands
from bs4 import BeautifulSoup

initial_extensions = ['image', 'booru']

#ok so with this we can have Tenshi also respond to the = prefix, i'll leave this enabled for a short time then switch to just mention
#bot = commands.Bot(command_prefix=commands.when_mentioned_or('='), case_insensitive=True)
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
bot.remove_command("help")

#Sharding! should help with performance since the bot is on 1000+ servers
client = discord.AutoShardedClient()

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


#Prefix
#tb_prefix = ('<@' + client.user.id + '> ')

#bot will display this on startup when accepting commands

@bot.event
async def on_ready():
    print(' ')
    print('TenshiBot startup complete ')
    print(' ')
    print('User ID - ' + str(bot.user.id))
    print('Username - ' + bot.user.name)
    print('Shard Count - ' + str(bot.shard_count))
    print('TenshiBot Ver - ' + bot_version)
    print('System Variant - ' + bot_variant)
    print(' ')
    print('servercount - ' + str(len(bot.guilds)))
    print(discord.version_info)
    await bot.change_presence(activity=discord.Game(name="Startup complete"))
    await asyncio.sleep(7)
    await bot.change_presence(activity=discord.Streaming(name="TenshiBot", url='https://twitch.tv/99710'))

    
#error event code
#print the error to the console and inform the user   
@bot.event
async def on_command_error(ctx, error):
    #command not failed
    if isinstance(error, commands.CommandNotFound):
        return
    #user failed owner check
    if isinstance(error, commands.CheckFailure):
        await ctx.send("not owner")
    else:
        print(error)
        await ctx.send(error)

#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)

#command logging
@bot.event
async def on_command(ctx):
    print(ctx.message.content)
    return

#owner check
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 166189271244472320
    return commands.check(predicate)

#bot added/kicked from server messages
@bot.event
async def on_guild_join(guild):
        print("[Info] New server get! - " + str(guild))
        
@bot.event
async def on_guild_remove(guild):
        print("[Info] Kicked from a server - " + str(guild))

    
#help command
@bot.command()
async def help(ctx):
    hlp = open("help_cmd.txt", "r")
    help_cmd = hlp.read()
    await ctx.send(help_cmd)        

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#nsfw flag check
@bot.command()
async def nsfwtest(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send('nsfw')
    else:
        await ctx.send('not nsfw')

@bot.command()
@is_owner()
async def ping2(ctx):
    await ctx.send('pong')    

@bot.command()
async def errortest(ctx):
    await()


#basic admin functionality
@bot.command()
@is_owner()    
async def vpsreboot(ctx):
    #os.system("sudo reboot")
    os.system("shutdown -r -t 30")
    await ctx.send('Rebooting the VPS')

#ban test command
@bot.command()
@is_owner()
async def bantest(ctx):
    await ctx.author.ban(reason=':)')
    await ctx.author.unban

#console command
@bot.command()
@is_owner()
#freezes the bot!
async def console(ctx):
    cmd=ctx.message.content[len("<@571094749537239042> console"):].strip()
    result = subprocess.check_output([cmd], stderr=subprocess.STDOUT)
    #os.system(ctx.message.content)
    await ctx.send(result)    
    

#this has to be at the end of the code
#client.run(token)
tkn = open("test/token_debug.txt", "r")
#tkn = open("test/token_production.txt", "r")
token = tkn.read()
tkn.close()    
bot.run(token, bot=True, reconnect=True)
