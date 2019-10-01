"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import json
import asyncio

from discord.ext import commands as comms
import discord

from modules.output import path, cs


class Google_Requester(comms.Cog):
    """Fetching information from Google: Youtube."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.group(enabled=False)
    async def google(self, ctx):
        """The Google group command.

        Returns:
            The built-in help command if no command is invoked

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **;help {ctx.command}** for help')

    @comms.command()
    async def yt(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Google_Requester(bot))
