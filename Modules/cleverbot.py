#Tenshibot Cleverbot module
#based on https://github.com/crrapi/async-cleverbot/blob/master/examples/discord-py-cog.py

#ratelimiting options
#number of commands which can be ran in timeframe
rlimit_cmd = 1
#timeframe (seconds)
rlimit_time = 10
#

import discord
import asyncio
from discord.ext import commands
import async_cleverbot as ac


travitia_key = open("Tokens/cleverbot.txt", "r")
tr_key = travitia_key.read()

class cleverbotCog(commands.Cog):
    """Commands for interacting with the Travitia Cleverbot API"""

    def __init__(self, bot):
        self.bot = bot
        self.cleverbot = ac.Cleverbot(tr_key, context=ac.DictContext())
        self.cleverbot.set_context(ac.DictContext(self.cleverbot))

    @commands.command()
    @commands.cooldown(rlimit_cmd, rlimit_time, commands.BucketType.user)
    async def ai(self, ctx, *, query: str):
        ai_disable = discord.utils.get(message.guild.roles, name="tenko_disableai")
        """Ask Cleverbot a question!"""
        #disable AI command in TPL
        #if int(ctx.guild.id) == int("486699197131915264"):
            #await ctx.send('Error: AI command cannot be used in TPL')
        #disable ai command via role
        if ai_disable in message.guild.me.roles
            await ctx.send("`=ai` has been disabled on this server")
            return
        
        await ctx.trigger_typing()
        #print (ac.DictContext())
        try:
            r = await self.cleverbot.ask(query, ctx.author.id)
        except ac.InvalidKey:
            return await ctx.send("An error has occurred. The API key provided was not valid.")
        except ac.APIDown:
            return await ctx.send("Celestials have to sleep sometimes. Please ask me later!")
        else:            
            await ctx.send("{}, {}".format(ctx.author.mention, r.text))
         
#    @commands.Cog.listener()
#    async def on_message(self, message):

#        immersiveflag = discord.utils.get(message.guild.roles, name="tenko_immersiveai")
#        query = message.content[len("<@!" + str(self.bot.user.id) + ">"):].strip()
        #print(query)
#        if immersiveflag in message.guild.me.roles and message.content.startswith("<@!" + str(self.bot.user.id) + ">"):
#            try:
#                r = await self.cleverbot.ask(query, message.author.id)
#            except ac.InvalidKey:
#                return await message.channel.send("An error has occurred. The API key provided was not valid.")
#            except ac.APIDown:
#                return await message.channel.send("Celestials have to sleep sometimes. Please ask me later!")
#            else:            
#                await message.channel.send("{}, {}".format(message.author.mention, r.text))
#                return
    

    def cog_unload(self):
        self.bot.loop.create_task(self.cleverbot.close())


def setup(bot):
    bot.add_cog(cleverbotCog(bot))
