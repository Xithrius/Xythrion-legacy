'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import platform
import datetime
import asyncio

import discord
from discord.ext import commands as comms

from scraping.yahoo_finance import get_stock_summary
# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
# Stock cog
# ////////////////////////
# Getting stocks from yahoo finance at the close time
# ///////////////////////////////////////////////////////// #


class StockCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.group()
    async def stocks(self, ctx, abbreviation, option='low'):
        stock_dict = get_stock_summary(abbreviation, option)
        for k, v in stock_dict.items():
            if k == 'Title':
                embed = discord.Embed(title=f'Summary for the stock of {v[0]}', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))
            else:
                try:
                    embed.add_field(name=k, value=v[0], inline=False)
                except IndexError:
                    pass
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @stocks.command()
    async def remind(self, ctx):
        await ctx.send(datetime.datetime.now() + datetime.timedelta(hours=7))

    @stocks.command()
    async def cancel(self, ctx):
        pass


def setup(bot):
    bot.add_cog(StockCog(bot))
