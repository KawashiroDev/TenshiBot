#Tenshibot Cleverbot module
#based on https://github.com/crrapi/async-cleverbot/blob/master/examples/discord-py-cog.py

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 1
#timeframe (seconds)
rlimit_time = 10
#

import discord
from discord.ext import commands
import async_cleverbot as ac

travitia_key = open("Tokens/cleverbot.txt", "r")
tr_key = travitia_key.read()

class Cleverbot(commands.Cog):
    """Commands for interacting with the Travitia Cleverbot API"""

    def __init__(self, bot):
        self.bot = bot
        self.cleverbot = ac.Cleverbot(tr_key)
        self.cleverbot.set_context(ac.DictContext(self.cleverbot))

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ai(self, ctx, *, query: str):
        """Ask Cleverbot a question!"""
        await ctx.trigger_typing()
        try:
            r = await self.cleverbot.ask(query, ctx.author.id)
        except ac.InvalidKey:
            return await ctx.send(
                "An error has occurred. The API key provided was not valid."
            )
        except ac.APIDown:
            return await ctx.send("Celestials have to sleep sometimes. Please ask me later!")
        else:            
            await ctx.send("{}, {}".format(ctx.author.mention, r.text))

    def cog_unload(self):
        self.bot.loop.create_task(self.cleverbot.close())


def setup(bot):
    bot.add_cog(Cleverbot(bot))
