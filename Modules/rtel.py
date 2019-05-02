#TenshiBot RTEL module

import discord
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands


class rtelCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def jojo(ctx, arg):
    await ctx.send(arg + ' has been stopped!', file=discord.File('pics/stop.jpg'))

@commands.command()
async def banana(ctx, arg):
    await ctx.send(arg + ' has been banaed!', file=discord.File('pics/banana.png'))

@commands.command()
async def oil(ctx, arg):
    await ctx.send(arg + ' has been oiled!', file=discord.File('pics/oil.png'))

@commands.command()
async def confused(ctx, arg):
    await ctx.send(file=discord.File('pics/confused.png'))

@commands.command()
async def thonk(ctx, arg):
    await ctx.send(file=discord.File('pics/thonk.gif'))    


					                    

def setup(bot):
    bot.add_cog(rtelCog(bot))
