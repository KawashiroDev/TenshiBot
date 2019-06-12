#TenshiBot debug module
#Only loaded if Tenshi is in debug mode!!

import discord
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands


class debugCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def d_test(self, ctx):
        await ctx.send('ok!')
    
					                    

def setup(bot):
    bot.add_cog(debugCog(bot))
