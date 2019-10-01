"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sqlite3

from discord.ext import commands as comms

from modules.output import path


class Message_Recorder(comms.Cog):
    """Fetching map information from Google."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command()
    async def rank(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Message_Recorder(bot))
