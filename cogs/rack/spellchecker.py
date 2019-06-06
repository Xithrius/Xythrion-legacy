'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform
import time
import pytemperature
import json
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Spellchecker cog
# //////////////////////////////////////////////////////////////////////////// #
# Correcting people's spelling
# //////////////////////////////////////////////////////////////////////////// #


class Spellchecker_Cog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot

    """

    Commands

    """
    async def disable_spellchecker(self, ctx):
        """
        Disables spellchecker for a specific user
        """
        embed = discord.Embed(title=f'`Will no longer check spelling for` {ctx.message.author}', colour=0xc27c0e, timestamp=now())
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)
        with open(path('rehasher', 'configuration', 'blockd_spellchecking.txt'), 'a') as f:
            f.write(ctx.message.author)

    """

    Events

    """
    @comms.Cog.listener()
    async def on_message(self, message):
        if message.content == 'tes':
            pass
            # replace with the correct word, 'test'


def setup(bot):
    bot.add_cog(Spellchecker_Cog(bot))
