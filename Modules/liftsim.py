#TenshiBot liftsim module

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 2
#timeframe (seconds)
rlimit_time = 60

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

class liftsimCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.default)
    async def liftsim(self, ctx, *, args):
        
        if args == "ecodisc":
            await ctx.send('kone_ecodisc_placeholder')
            return

        if args == "blindvf":
            await ctx.send('blindvfdrive_placeholder')
            return

        else:
            await ctx.send('invalid model')
            return
    

def setup(bot):
    bot.add_cog(liftsimCog(bot))
