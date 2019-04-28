#TenshiBot Slipstream version

#this version is still in early development and NOT ready to replace the main version

#todo
#server count display and posting
#dev id checking for some commands


##Parameters##

#token
tkn = open("test/token.txt", "r")
token = tkn.read()
tkn.close()

#booru URL, used for touhou images and safebooru command
booru = 'safebooru.org'

#booru rating
#options are: safe, questionable, explicit
#affects the safebooru command only
boorurating = 'safe'

#booru tag blacklist
#results which have these tags won't be shown in the touhou commands
#does not affect the safebooru command
boorublacklist = '-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini'

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
booruappend = 'http:'

#Discordbots.org API key
dbo_api = ''

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.5'

#prefix
#Debug account has user ID 571094749537239042
#Normal account has user ID 252442396879486976
tb_prefix = ('<@571094749537239042> ')


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


#bot = commands.Bot(command_prefix= '<@' + str(bot.user.id) + '> ')
#do not leave '' here

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
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Bhava-agra As Seen Through a Childs Mind'))
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
bot.run(token, bot=True, reconnect=True)
