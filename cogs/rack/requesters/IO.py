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
import json
import aiohttp
import cv2
import os

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Input/request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from other user's input
# //////////////////////////////////////////////////////////////////////////// #


class IO_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.group()
    async def meme(self, ctx):
        await ctx.send(file=discord.File(path('tmp', 'plots', 'plot.png')))

    @meme.command()
    async def help(self, ctx):
            """
            Gives the user information on how the meme input/output works
            """
            embed = discord.Embed(title='', colour=0xc27c0e, timestamp=now())
            help = '''
            `$ <> <>`
            `<>`: ``
            `<>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    """

    Events

    """
    @comms.Cog.listener()
    async def on_message(self, message):
        try:
            if (any(i in message.attachments[0].filename for i in ['.jpg', '.png', '.jpeg'])) and (not message.guild):
                for (dirpath, dirnames, filenames) in os.walk(path('repository', 'memes')):
                    pass
        except (IndexError, AttributeError):
            pass


def setup(bot):
    bot.add_cog(IO_Requester(bot))
