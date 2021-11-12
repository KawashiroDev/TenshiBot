#TenshiBot slash command module

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 5
#timeframe (seconds)
rlimit_time = 10
#

import discord
print("[debug] discord imported")
import aiohttp
import asyncio

from discord.ext import commands
print("[debug] commands imported")
from discord.commands import slash_command
print("[debug] slash commands imported")




class slashCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @slash_command() # Not passing in guild_ids creates a global slash command (might take an hour to register).
    async def test(self, ctx):
        await ctx.respond("that's not it")


					                    

def setup(bot):
    bot.add_cog(slashCog(bot))
