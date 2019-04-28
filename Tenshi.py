#TenshiBot Slipstream version

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

import discord
import requests
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands
from bs4 import BeautifulSoup

initial_extensions = ['image']

#ok so with this we can have Tenshi also respond to the = prefix, i'll leave this enabled for a short time then switch to just mention
#Leave error code commented out until = is disabled because that'll cause chaos
bot = commands.Bot(command_prefix=commands.when_mentioned_or('='), case_insensitive=True)
#bot = commands.Bot(command_prefix=commands.when_mentioned, case_insensitive=True)
#bot = commands.Bot(command_prefix= tb_prefix, case_insensitive=True)
client = discord.client

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
#uncomment when = prefix is removed    
#@bot.event
#async def on_command_error(ctx, error):
#    print(error)
#    await ctx.send(error)

#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)

    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def errortest(ctx):
    await()    
    

#this has to be at the end of the code
#client.run(token)
tkn = open("test/token.txt", "r")
token = tkn.read()
tkn.close()    
bot.run(token, bot=True, reconnect=True)
