#TenshiBot messaging module

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 2
#timeframe (seconds)
rlimit_time = 60

#Account age options
#How many days old the account needs to be 
dayspassed = 5

import discord
import aiohttp
import praw
import lxml
import random
import asyncio
import datetime 

from discord.ext import commands
from urlextract import URLExtract
from profanityfilter import ProfanityFilter
from datetime import datetime, timedelta

#url extractor stuff
extractor = URLExtract()

pf = ProfanityFilter()
pf_extended = ProfanityFilter(extra_censor_list=["@"])

user_blacklist = open("txt/badactors.txt", "r")
badactors = user_blacklist.read()

acc_age = datetime.now() - timedelta(days=dayspassed)

#owner check
#19/05 U+1F382
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 166189271244472320
    return commands.check(predicate)

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

class messagingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def messagedev(self, ctx, *, args):
        userid = str(ctx.author.id)
        username = str(ctx.author.name)
        yuyuko = self.bot.get_user(166189271244472320)
        devmsg = ('[' + ctx.author.name + '] ' + args)
        
#        if str(ctx.author.id) in badactors:
#            await ctx.send('Error: You have been blacklisted')
#            return
        if ctx.author.created_at > acc_age:
            await ctx.send('Error: Your Discord account is too new')
            return

        else:
            em = discord.Embed(colour=0x3ef1fa)
            em.set_author(name='Message recieved from a user', icon_url=self.bot.user.avatar_url)
            em.add_field(name="Message", value=args, inline=False)
            em.add_field(name="Users name", value=username, inline=False)
            em.add_field(name="Users ID", value=userid, inline=False)
            em.set_footer(text="You can reply using `messageuser <id>`")
            await yuyuko.send(embed=em)
            await ctx.send('\U0001F4E4 Message sent')
            return

    @commands.command()
    @is_owner()
    async def messageuser(self, ctx, userid, *, args):
        print(userid)
        print(args)
        
        yuyuko = self.bot.get_user(int(userid))
        em = discord.Embed(description = args, colour=0x3ef1fa)
        em.set_author(name='\U0001F4E8 Message from bot dev')
        em.set_footer(text="You can reply using `messagedev`")
        await yuyuko.send(embed=em)
        await ctx.send('\U0001F4E4 Message sent')
        return
    

def setup(bot):
    bot.add_cog(messagingCog(bot))
