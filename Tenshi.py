#TenshiBot Slipstream version
#Created by 99710


##Parameters##

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '2.0.4'

#Booting text
print('Please wait warmly...')

#owner id

import discord
import requests
import aiohttp
import random
import asyncio
import os
import subprocess
import cleverbot_io
import time

from discord.ext import commands
from random import randint

initial_extensions = ['Modules.image', 'Modules.booru']

#ok so with this we can have Tenshi also respond to the = prefix, i'll leave this enabled for a short time then switch to just mention
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('='), case_insensitive=True, shard_count=4)
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
bot.remove_command("help")

#Sharding! should help with performance since the bot is on 1000+ servers
client = discord.AutoShardedClient()

st = time.time()

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


#Discordbots.org API stuff
tkn_dbo = open("Tokens/dbl_api.txt", "r")
token_dbo = tkn_dbo.read()
tkn_dbo.close() 
dbltoken = token_dbo
url = ("https://discordbots.org/api/bots/252442396879486976/stats")
headers = {"Authorization" : dbltoken}        


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
    payload = {"server_count"  : str(len(bot.guilds))}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data=payload, headers=headers)
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
    print("[command] " + ctx.message.content[len("="):].strip() + " / " + str(ctx.guild))
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
        payload = {"server_count"  : str(len(bot.guilds))}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
        
@bot.event
async def on_guild_remove(guild):
        print("[Info] Kicked from a server - " + str(guild))
        payload = {"server_count"  : str(len(bot.guilds))}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url, data=payload, headers=headers)
    
#help command
@bot.command()
async def help(ctx):
    hlp = open("txt/help.txt", "r")
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


@bot.command()
async def about(ctx):
    second = time.time() - st
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)

    em = discord.Embed(title='Currently on ' + str(len(bot.guilds)) + ' servers', description='Uptime= %d weeks,' % (week) + ' %d days,' % (day) + ' %d hours,' % (hour) + ' %d minutes,' % (minute) + ' and %d seconds.' % (second) + '\n Created by 99710', colour=0x00ffff)
    em.set_author(name='TenshiBot ' + bot_version , icon_url=bot.user.avatar_url)
    await ctx.send(embed=em)

@bot.command()
async def invite(ctx):
    await ctx.send('Use this link to add me to your server: <https://discordapp.com/oauth2/authorize?client_id=252442396879486976&scope=bot&permissions=67161152>')    

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
    await ctx.send(args)

@bot.command()
async def dsay(ctx, *, args):
    await ctx.send(args)
    await ctx.message.delete()


@bot.command()
async def patreon(ctx):
    await ctx.send('Want to support TenshiBot on patreon? \nPatreon donators get featued in the help command as well as a donator role in the TenshiBot Hangout Discord\nhttp://patreon.com/tenshibot')    


@bot.command()
async def jojo(ctx, arg):
    await ctx.send(arg + ' has been stopped!', file=discord.File('pics/stop.jpg'))

@bot.command()
async def banana(ctx, arg):
    await ctx.send(arg + ' has been banaed!', file=discord.File('pics/banana.png'))

@bot.command()
async def oil(ctx, arg):
    await ctx.send(arg + ' has been oiled!', file=discord.File('pics/oil.png'))

@bot.command()
async def confused(ctx):
    await ctx.send(file=discord.File('pics/confused.jpg'))

@bot.command()
async def hooray(ctx):
    await ctx.send(file=discord.File('pics/hooray.png'))    

@bot.command()
async def thonk(ctx):
    await ctx.send(file=discord.File('pics/thonk.gif'))


cb_user = ''
cb_key = ''
cb_nick = 'Tenko_Slipstream'

#@bot.command
#async def ai(ctx):
#    ai2 = cleverbot_io.set(user= cb_user , key= cb_key , nick= cb_nick )
    #this cleverbot engine has a delay so send a typing status to look like something is happening
    #await client.send_typing(channel)
#    answer = (ai2.ask(ctx.message.content[len("<@571094749537239042> ai"):].strip()))
    #await client.send_typing(channel)
#    await ctx.send(answer)

#this has to be at the end of the code
#client.run(token)
#tkn = open("Tokens/tenshi_debug.txt", "r")
tkn = open("Tokens/tenshi_production.txt", "r")
token = tkn.read()
tkn.close()    
bot.run(token, bot=True, reconnect=True)
