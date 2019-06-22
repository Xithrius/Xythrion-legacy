'''
>> ARi0
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
import json
import asyncio
import threading

from discord.ext import commands as comms
import discord

from ARi0.containers.QOL.shortened import now
from ARi0.containers.QOL.pathing import path
from ARi0.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Spotify detector cog
# //////////////////////////////////////////////////////////////////////////// #
# Messages the user about spotify updates
# //////////////////////////////////////////////////////////////////////////// #

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# Don't look at this monstrosity!
# It is really messy and no where near finished
# Please don't judge it, just yet
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #


class Spotify_Detector(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.background_service = self.bot.loop.create_task(self.update_detector())
        with open(path('repository', 'user_config', 'spotify.json'), 'r') as f:
            self.spotify_list = json.load(f)

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.background_service.cancel()

    """

    Background tasks

    """
    async def update_detector(self):
        """

        """
        await self.bot.wait_until_ready()
        # while not self.bot.is_closed():
        if not self.bot.is_closed():
            pass

    """

    Commands

    """
    @comms.group()
    async def spotify(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You can either enable or disable spotify notifications through discord. **There are no other options.**')

    @spotify.command()
    async def enable(self, ctx):
        self.spotify_list.append(ctx.message.author)

    @spotify.command()
    async def disable(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Spotify_Detector(bot))
