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

        
#test the booru img embed with various URL's
    @commands.command()
    async def imgembed(self, ctx, arg):
        em = discord.Embed(title='', description='', colour=0x42D4F4)
        em.set_author(name='imgembed')
        em.set_image(url=arg)
        await ctx.send(embed=em)

#test the booru img embed with various URL's
    @commands.command()
    async def embedcol(self, ctx, arg):
        em = discord.Embed(title='テスト', description='テスト', colour=discord.Colour(int(arg)))
        em.set_author(name='Sample_embed', icon_url=bot.user.avatar_url)
        await ctx.send(embed=em)
    
					                    

def setup(bot):
    bot.add_cog(debugCog(bot))
