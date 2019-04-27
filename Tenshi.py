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
import praw
import lxml

from discord.ext import commands
from bs4 import BeautifulSoup


#bot = commands.Bot(command_prefix= '<@' + str(bot.user.id) + '> ')

bot = commands.Bot(command_prefix= tb_prefix)


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



#this has to be at the end of the code
#client.run(token)
bot.run(token, bot=True, reconnect=True)
