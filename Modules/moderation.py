#Tenshibot moderation(?) module

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 1
#timeframe (seconds)
rlimit_time = 10
#

import discord
import asyncio
from discord.ext import commands


class modCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


         
    @commands.Cog.listener()
    async def on_message(self, message):

        filter_enable = discord.utils.get(message.guild.roles, name="tenko_filterchat")

        if message.content == "test":     
            await message.channel.send("Scam URL detected"))
            return
    


def setup(bot):
    bot.add_cog(modCog(bot))
