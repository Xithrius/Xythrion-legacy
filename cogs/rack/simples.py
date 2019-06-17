'''
>> SoftBot
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import datetime
import os

from discord.ext import commands as comms
import discord

from SoftBot.containers.QOL.shortened import now
from SoftBot.containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Simple cog
# //////////////////////////////////////////////////////////////////////////// #
# A cog for all the simple commands
# //////////////////////////////////////////////////////////////////////////// #


class Simples_Cog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    """
    Time
    """
    @comms.command()
    async def from_timestamp(self, ctx, stamp):
        dt_object = datetime.datetime.fromtimestamp(int(stamp))
        await ctx.send(f'**Date from timestamp:** {dt_object}')

    @comms.command()
    async def time(self, ctx):
        await ctx.send(f'**Current time:** {now()}')

    """

    Events

    """
    """
    Emoticons in text
    """
    @comms.Cog.listener()
    async def on_message(self, message):
        try:
            command_list = [f'${x[:-4]}' for x in os.listdir(path('repository', 'emoticons'))]
            if message.content.startswith(command_list):
                pass
        except:
            pass


def setup(bot):
    bot.add_cog(Simples_Cog(bot))
