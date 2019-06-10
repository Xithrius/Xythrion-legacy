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


import datetime

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now


# //////////////////////////////////////////////////////////////////////////// #
# <> request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from <>
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
    @comms.command()
    async def from_timestamp(self, ctx, stamp):
        dt_object = datetime.datetime.fromtimestamp(int(stamp))
        await ctx.send(f'**Date from timestamp:** {dt_object}')

    @comms.command()
    async def time(self, ctx):
        await ctx.send(f'**Current time:** {now()}')


def setup(bot):
    bot.add_cog(Simples_Cog(bot))
