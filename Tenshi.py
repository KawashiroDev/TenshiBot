#TenshiBot Slipstream version
#aka "that rewrite version that doesn't use musicbot base code"

#this version is still in early development and NOT ready to replace the main version

#todo
#ignore other bots
#server count display and posting
#dev id checking for some commands


##Parameters##

#Token
token = ''

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.5'

#prefix
#i tried not hardcoding this, it didn't work so here we are
tb_prefix = ('<@225323275163664384> ')

print('Please wait warmly...')

import discord
import requests

client = discord.Client()


#Prefix
#Tenshi's Prefix, this has to be below the imports
#ok, so i want this to be a mention and actually work this time, nvm it doesn't
#tb_prefix = ('<@' + client.user.id + '> ')

#bot will display this on startup when accepting commands
@client.event
async def on_ready():
    print(' ')
    print('TenshiBot startup complete ')
    print(' ')
    print('System ID - ' + client.user.id)
    print('System Name - ' + client.user.name)
    print('System Ver - ' + bot_version)
    print('System Variant - ' + bot_variant)
    print(' ')

    print('servercount - ' + str(len(client.servers)))



#discard other bot commands
#async def on_message():
#    if mesage.author.bot:
#        return


#test command
@client.event
async def on_message(message):

#checks if the message starts with the prefix and the command
    if message.content.startswith(tb_prefix + 'helloworld'):
#prints the message to the console
        print(message.content)
#sends the response
        await client.send_message(message.channel, "bhava-agra")



#this has to be at the end of the code
client.run(token)
