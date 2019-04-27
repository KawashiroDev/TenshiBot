#TenshiBot Slipstream version
#aka "that rewrite version that doesn't use musicbot base code"

#this version is still in early development and NOT ready to replace the main version

#todo
#server count display and posting
#dev id checking for some commands


##Parameters##

#Token
#perhaps i can read this from an external file?
tkn = open("test/token.txt", "r")
token = tkn.read()
#token = ''

#Discordbots.org API key
dbo_api = ''

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.5'

#prefix
#Debug account has user ID 571094749537239042
#Normal account has user ID 252442396879486976
#i tried not hardcoding this, it didn't work 
tb_prefix = ('<@571094749537239042> ')
#tb_prefix = ('<@' + str(bot.user.id) + '>')


#Booting text
print('Please wait warmly...')

import discord
import requests

from discord.ext import commands


#bot = commands.Bot(command_prefix= '<@' + str(bot.user.id) + '> ')
bot = commands.Bot(command_prefix= 'tb_prefix')
client = discord.Client()

#Prefix
#Tenshi's Prefix, this has to be below the imports
#ok, so i want this to be a mention and actually work this time, nvm it doesn't
#tb_prefix = ('<@' + client.user.id + '> ')

#bot will display this on startup when accepting commands
#NTS: Try using bot where there would normally be client eg client.user.name > bot.user.name

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
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.author.bot:
        return

#test commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)



#this has to be at the end of the code
#client.run(token)
bot.run(token, bot=True, reconnect=True)
