"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import json
import asyncio

from discord.ext import commands as comms
from google.cloud import texttospeech
import discord

from modules.output import path, ds


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('config', 'gsc.json')
with open(path('config', 'config_connections.json')) as f:
    ffmpeg_options = json.load(f)['ytdl']['ffmpeg_options']


class Google_Requester(comms.Cog):
    """Fetching map information from Google."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.group()
    async def google(self, ctx):
        """The Google group command.

        Returns:
            The built-in help command if no command is invoked

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **;help {ctx.command}** for help')

    @google.command()
    async def youtube(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Google_Requester(bot))
