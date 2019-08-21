#TenshiBot Slipstream version
#Created by 99710


##Parameters##

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '2.2.7'

#Booting text
print('Please wait warmly...')

#windows check
#if this directory exists then run in debug mode
#if not then run in production mode
win_dir_check = '/windows'

#owner id

import discord
import requests
import aiohttp
import random
import asyncio
import os
import subprocess
#import cleverbot_io
import time
#import Cleverbotio
import traceback
import praw
import lxml
#import saucenaopy
import twitter

from discord.ext import commands
from random import randint
from bs4 import BeautifulSoup
#from Cleverbotio import 'async' as cleverbot
#from saucenaopy import SauceNAO

#https://www.microsoft.com/en-us/download/details.aspx?id=48159
from profanityfilter import ProfanityFilter

#Windows or linux check
#used to autoswitch the bot between debug/production modes

if (os.path.isdir(win_dir_check)) == True:
    print('[Startup] Detected a windows PC, running in debug mode')
    bot_mode = 'Debug'
    initial_extensions = ['Modules.image', 'Modules.booru', 'Modules.debug']
    print('[Debug] /Modules/debug.py loaded')
else:
    print('[Startup] Running in production mode')
    bot_mode = 'Production'
    initial_extensions = ['Modules.image', 'Modules.booru']

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
"You seen John Connor around here? Tell him i said hi",
#"CrashOverride? What kind of username is that?",
#"ZeroCool? Sounds like one of Cirno's aliases",
"Wait... Yukari is here?",
"Chang'e are you watching? \nSome fox lady said hi",
"Hold on a sec i just saw Sakuya with some coffee",
"Guys the thermal drill, go get it",
"!",
"!!",
"?!",

"*Stares*",
"*Looks around*",
"*Stares at you*",
#"*Eating a peach~*",
"*Is eating a peach~*",
"*Is eating a corndog~*",
"*Is looking at Shion~*",
"*Is playing with Shion's hair~*",
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
]

shuffle_test = [
"avatars/test/1.png",
"avatars/test/2.png",
"avatars/test/3.png",
"avatars/test/4.png",
]


#Disable sharding and = prefix if in debug mode
#if you want to have the bot run as normal on a windows machine then change the windows folder check to a non existent folder
if (os.path.isdir(win_dir_check)) == True:
    bot = commands.Bot(command_prefix=commands.when_mentioned, case_insensitive=True)
else:
    bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('='), case_insensitive=True, shard_count=4)
#bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, case_insensitive=True)
#removes the built in help command, we don't need it
bot.remove_command("help")

#Sharding! should help with performance since the bot is on 1000+ servers
client = discord.AutoShardedClient()
#client = discord.Client()

st = time.time()

pf = ProfanityFilter()

t_api = open("Tokens/twitter_consumer.txt", "r")
tw_api = t_api.read()
t_secret = open("Tokens/twitter_consumer_secret.txt", "r")
tw_secret = t_secret.read()
t_access = open("Tokens/twitter_access.txt", "r")
tw_access = t_access.read()
t_access_secret = open("Tokens/twitter_access_secret.txt", "r")
tw_access_secret = t_access_secret.read()



api = twitter.Api(consumer_key=tw_api,
consumer_secret=tw_secret,
access_token_key=tw_access,
access_token_secret=tw_access_secret)



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
if (os.path.isdir(win_dir_check)) == True:        
    tkn_dbo = open("Tokens/dbl_api_blank.txt", "r")
else:
    tkn_dbo = open("Tokens/dbl_api.txt", "r")
token_dbo = tkn_dbo.read()
tkn_dbo.close() 
dbltoken = token_dbo
url = ("https://discordbots.org/api/bots/252442396879486976/stats")
headers = {"Authorization" : dbltoken}        


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
    print('System Mode - ' + bot_mode)
    print(' ')
    print('servercount - ' + str(len(bot.guilds)))
    print(discord.version_info)
    payload = {"server_count"  : str(len(bot.guilds))}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(url, data=payload, headers=headers)
    await bot.change_presence(activity=discord.Game(name="Startup Complete"))
    await asyncio.sleep(7)
    #await bot.change_presence(activity=discord.Streaming(name="TenshiBot", url='https://twitch.tv/99710'))
    await bot.change_presence(activity=discord.Game(name="TenshiBot"))

    
#error event code
#print the error to the console and inform the user   
@bot.event
async def on_command_error(ctx, error):
    #command not found
    if isinstance(error, commands.CommandNotFound):
        return
    #user has invalid permissions
    if isinstance(error, commands.MissingPermissions):
        #em = discord.Embed(title='Error', description = error, colour=0xc91616)
        #em.set_author(icon_url=bot.user.avatar_url)
        #await ctx.send(embed=em)
        await ctx.send(error)
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

    #none of the above         
    else:
        print(error)
        #print(str(traceback.print_exc()))
        errormsg = await ctx.send("An error has occured, The dev has been notified")
        #todo: actually put code here that notifies me

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


secure_random = random.SystemRandom()
#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    #non command test
    #debug id - 571094749537239042
    #production id - 252442396879486976

    #! is needed if Tenshi has a nickname set on the server
    if message.content == '<@252442396879486976>':
        await message.channel.send(secure_random.choice(mentioned_nomsg))
        print("[command] mention_nomsg")
    if message.content == '<@!252442396879486976>':
        await message.channel.send(secure_random.choice(mentioned_nomsg))
        print("[command] mention_nomsg")

#'f' command uses on_message instead of async def due to ayana clash
    if message.content == '<@252442396879486976> f':
        if '@everyone' in message.author.display_name:
            await message.channel.send(message.author.display_name + ' has paid their respects')
            print("[command] f")
            return
        if '@here' in message.author.display_name:
            await message.channel.send('`' + message.author.display_name + '` has paid their respects')
            print("[command] f")
            return
        else:
            await message.channel.send('`' + message.author.display_name + '` has paid their respects')
            print("[command] f")
            return
    if message.content == '<@!252442396879486976> f':
        if '@everyone' in message.author.display_name:
            await message.channel.send('`' + message.author.display_name + '` has paid their respects')
            print("[command] f")
            return
        if '@here' in message.author.display_name:
            await message.channel.send('`' + message.author.display_name + '` has paid their respects')
            print("[command] f")
            return
        else:
            await message.channel.send(message.author.display_name + ' has paid their respects')
            print("[command] f")
            return



#    print(message.content)
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
        return ctx.author.id == 166189271244472320
    return commands.check(predicate)

#TenshiBot Hangout check (the name of the Tenshi's server)
def is_hangout():
    async def predicate(ctx):
        return ctx.guild.id == 273086604866748426
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
    await bot.send_typing(channel)


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

@bot.command()
@is_owner()
async def asciitest(ctx, *, args):
    asciitext = strip_non_ascii(args)
    if asciitext == '':
        await ctx.send('invalid char')
    else:
        await ctx.send(asciitext)
    

@bot.command()
async def sendtweet(ctx, *, args):
    #convert text to ascii
    asciitext = strip_non_ascii(args)
    asciiusername = strip_non_ascii(ctx.author.name)
    if asciitext == '':
        await ctx.send('Error: Tweet contains no alphanumeric characters')
    #check username for profanity
    if pf.is_profane(asciiusername) == True:
        await ctx.send('Error: Your Discord username is unsupported')
        return
    #link check
    if 'https://' in asciitext:
        if 'https://www.youtube.com/' not in asciitext:
            await ctx.send('Error: Tweet contains an unsupported link')
            return
        else:
            em = discord.Embed(title='Are you sure you want to tweet this?', description = asciitext, colour=0x6aeb7b)
            em.set_author(name='KawashiroLink Subsystem' , icon_url=bot.user.avatar_url)
            tweetconfirm = await ctx.send(embed=em)
        #tweetconfirm = await ctx.send('Are you sure you want to tweet this?')
        #add tick and X reactions for user to react to
            await tweetconfirm.add_reaction('\U00002705')
            await tweetconfirm.add_reaction('\U0000274e')

            def ays_tweet(reaction, user):
                return (user == ctx.author and str(reaction.emoji) == '\U00002705') or (user == ctx.author and str(reaction.emoji) == '\U0000274e')
                                   
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30, check=ays_tweet)
            except asyncio.TimeoutError:
                await ctx.send('Error: Timed out waiting for user response')
                return
            else:
                if ((reaction.emoji) == '\U00002705') and reaction.message.id == tweetconfirm.id:
                    #Profanity check tweet and add username before sending
                    finaltweet = ('[' + ctx.author.name + '] ' + pf.censor(asciitext))
                    api.PostUpdate(finaltweet)
                    print('[tweet] "' + finaltweet + '" User ID: :' + str(ctx.author.id))
                    await ctx.send('Tweet Posted')
                    return
                elif ((reaction.emoji) == '\U0000274e'):
                    await ctx.send('Operation canceled')
                    return

    if 'www.' in asciitext:
        if 'www.youtube.com/' not in asciitext:
            await ctx.send('Error: Tweet contains an unsupported link')
            return
        else:
            em = discord.Embed(title='Are you sure you want to tweet this?', description = asciitext, colour=0x6aeb7b)
            em.set_author(name='KawashiroLink Subsystem' , icon_url=bot.user.avatar_url)
            tweetconfirm = await ctx.send(embed=em)
        #tweetconfirm = await ctx.send('Are you sure you want to tweet this?')
        #add tick and X reactions for user to react to
            await tweetconfirm.add_reaction('\U00002705')
            await tweetconfirm.add_reaction('\U0000274e')

            def ays_tweet(reaction, user):
                return (user == ctx.author and str(reaction.emoji) == '\U00002705') or (user == ctx.author and str(reaction.emoji) == '\U0000274e')
                                   
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=30, check=ays_tweet)
            except asyncio.TimeoutError:
                await ctx.send('Error: Timed out waiting for user response')
                return
            else:
                if ((reaction.emoji) == '\U00002705') and reaction.message.id == tweetconfirm.id:
                    #Profanity check tweet and add username before sending
                    finaltweet = ('[' + ctx.author.name + '] ' + pf.censor(asciitext))
                    api.PostUpdate(finaltweet)
                    print('[tweet] "' + finaltweet + '" User ID: :' + str(ctx.author.id))
                    await ctx.send('Tweet Posted')
                    return
                elif ((reaction.emoji) == '\U0000274e'):
                    await ctx.send('Operation canceled')
            
            
    else:
        
        em = discord.Embed(title='Are you sure you want to tweet this?', description = asciitext, colour=0x6aeb7b)
        em.set_author(name='KawashiroLink Subsystem' , icon_url=bot.user.avatar_url)
        tweetconfirm = await ctx.send(embed=em)
        #tweetconfirm = await ctx.send('Are you sure you want to tweet this?')
        #add tick and X reactions for user to react to
        await tweetconfirm.add_reaction('\U00002705')
        await tweetconfirm.add_reaction('\U0000274e')

        def ays_tweet(reaction, user):
            return (user == ctx.author and str(reaction.emoji) == '\U00002705') or (user == ctx.author and str(reaction.emoji) == '\U0000274e')
                                   
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30, check=ays_tweet)
        except asyncio.TimeoutError:
            await ctx.send('Error: Timed out waiting for user response')
            return
        else:
            if ((reaction.emoji) == '\U00002705') and reaction.message.id == tweetconfirm.id:
                #Profanity check tweet and add username before sending
                finaltweet = ('[' + ctx.author.name + '] ' + pf.censor(asciitext))
                api.PostUpdate(finaltweet)
                print('[tweet] "' + finaltweet + '" User ID: :' + str(ctx.author.id))
                await ctx.send('Tweet Posted')
                return
            elif ((reaction.emoji) == '\U0000274e'):
                await ctx.send('Operation canceled')

@bot.command()
@is_owner()
async def sendtweet2(ctx, *, args):
    api.PostUpdate(args)
    await ctx.send('posted')

@bot.command()
@is_owner()
async def dumptwitterinfo(ctx):
    await ctx.send(api.VerifyCredentials())

@bot.command()
@is_owner()
async def censortest(ctx, *, args):
    await ctx.send(pf.censor(args))

@bot.command()
@is_owner()
async def censortestascii(ctx, *, args):
    asciitext = strip_non_ascii(args)
    await ctx.send(pf.censor(asciitext))    

@bot.command()
@is_owner()
async def extendedcensortest(ctx, *, args):
    await ctx.send(pf_extended.censor(args))    

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

@bot.command()
@is_owner()
async def ping2(ctx):
    await ctx.send('pong')

@bot.command()
@is_hangout()
async def ping3(ctx):
    await ctx.send('ok')    

@bot.command()
async def errortest(ctx):
    await()


#basic admin functionality
@bot.command()
@is_owner()    
async def vpsreboot(ctx):
    await bot.change_presence(activity=discord.Game(name="Rebooting..."))
    await ctx.send('Rebooting the VPS')
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
    await bot.change_presence(activity=discord.Streaming(name= args, url='https://twitch.tv/99710'))

@bot.command()
@is_owner()  
async def setstatus(ctx, *, args):
    await bot.change_presence(activity=discord.Game(name= args))
    await ctx.send("status set to " + "`" + args + "`")

@bot.command()
@is_owner()  
async def setname(ctx, *, args):
    await bot.user.edit(username= args)

@bot.command()
@is_owner()  
async def setnick(ctx, *, args):
    await bot.user.edit(nickname= args)
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
    await bot.user.edit(username="CirnoBot", avatar = newavatar.read())
    await bot.change_presence(activity=discord.Game(name="with Daiyousei"))
    await ctx.send("Enabled Cirnomode, Reset to Tenshi with `tenkomode`")

@bot.command()
@is_owner()
async def tenkomode(ctx):   
    image =  "avatars/normal/" + random.choice(os.listdir("avatars/normal"))
    newavatar = open(image, 'rb')
    await bot.user.edit(username="TenshiBot", avatar = newavatar.read())
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

#console command
@bot.command()
@is_owner()
#freezes the bot!
async def console(ctx):
    cmd=ctx.message.content[len("<@571094749537239042> console"):].strip()
    result = subprocess.check_output([cmd], stderr=subprocess.STDOUT)
    #os.system(ctx.message.content)
    await ctx.send(result)

#role creation testing command
#this may be intresting to have as a hangout exclusive command
#and let users make roles with custom colours

#role creation command V2, currently throws an error when trying to assign the role
@bot.command()
@is_owner()
async def makerole(ctx, colour):
    perms=discord.Permissions(0)
    col=discord.Colour(int(colour))
    userid=ctx.author.id
    await ctx.guild.create_role(name=userid, permissions=perms, colour=col, reason='role creation test')
    user=ctx.message.author
    role=discord.utils.get(ctx.guild.roles, name=str(userid))
    await user.add_roles(user, role)
   
@bot.command()
@is_owner()
async def makerole2(ctx, *, args):
    #refer to this for permissions values https://discordapi.com/permissions.html
    #it's best to leave this on 0 unless testing
    perms=discord.Permissions(0)
    #col=discord.Colour(510)
    #this also supports hex
    col=discord.Colour(args)
    await ctx.guild.create_role(name='test', permissions=perms, colour=col, reason='role creation test')
    #await ctx.guild.create_role(name='test')


#safebooru reaction support test
booru = 'safebooru.org'
boorurating = 'safe'
booruappend = ''
@bot.command()
async def safebooru_react(ctx, *, tags):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + tags) as r:
            if r.status == 200:
                soup = BeautifulSoup(await r.text(), "lxml")
                num = int(soup.find('posts')['count'])
                maxpage = int(round(num/100))
                page = random.randint(0, maxpage)
                t = soup.find('posts')
                p = t.find_all('post')
                if num == 0: 
                    msg = 'No posts found, are the tags spelt correctly?'
                    await ctx.send(msg)
                    return

                else:
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='', colour=0x42D4F4)
                    em.set_author(name='Booru image')
                    em.set_image(url=booruappend + msg)
                    sb_img = await ctx.send(embed=em)


                    def img_check(reaction, user):
                        return (str(reaction.emoji) == '\U0001f351')or(str(reaction.emoji) == '\U0000274c')
                                   
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=30, check=img_check)
                    except asyncio.TimeoutError:
                        return
                    else:
                        #x emoji
                        if ((reaction.emoji) == '\U0000274c') and reaction.message.id == sb_img.id:
                            await ctx.send("1")
                            await ctx.message.delete(sb_img)
                        #peach emoji    
                        if ((reaction.emoji) == '\U0001f351') and reaction.message.id == sb_img.id:
                            await ctx.send("2")
            else:
                msg = 'Safebooru is unavailable at this time'
                await ctx.send(msg)
                return    


@bot.command()
@is_owner()
async def saucenao(ctx, link):
    sauce = sn.get_sauce(link)
    await ctx.send(sauce)
    

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
async def about_adv(ctx):    
    await ctx.send('``` [about2] \n```')

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
    if "@everyone" in args:
        await ctx.send("`" + args + "`")
    if "@here" in args:
        await ctx.send("`" + args + "`")    
    else:
        await ctx.send(args)    

@bot.command()
async def dsay(ctx, *, args):
    if "@everyone" in args:
        await ctx.send("`" + args + "`")
        await ctx.message.delete()
    if "@here" in args:
        await ctx.send("`" + args + "`")
        await ctx.message.delete()    
    else:
        await ctx.send(args)    
        await ctx.message.delete()

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

#this has to be at the end of the code
#client.run(token)
if (os.path.isdir(win_dir_check)) == True:
    tkn = open("Tokens/tenshi_debug.txt", "r")
else:
    tkn = open("Tokens/tenshi_production.txt", "r")
token = tkn.read()
tkn.close()    
bot.run(token, bot=True, reconnect=True)
