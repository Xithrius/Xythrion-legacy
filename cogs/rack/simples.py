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


import datetime
import os

from discord.ext import commands as comms
import discord

from ARi0.containers.QOL.shortened import now
from ARi0.containers.QOL.pathing import path


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
    @comms.command()
    async def from_timestamp(self, ctx, stamp):
        dt_object = datetime.datetime.fromtimestamp(int(stamp))
        await ctx.send(f'**Date from timestamp:** {dt_object}')

    @comms.command()
    async def time(self, ctx):
        """

        """
        await ctx.send(f'**Current time:** {now()}')

    @comms.command(name='members')
    @comms.guild_only()
    async def get_members(self, ctx):
        """
        Get all users that exist within the guild
        """
        embed = discord.Embed(name=f'Members on the server', value=f'{ctx.message.guild}', colour=0xc27c0e, timestamp=now())
        embed.add_field(name='Members:', value=', '.join(str(x) for x in ctx.message.guild.members))
        await ctx.send(embed=embed)

    @comms.command(name='password')
    async def random_password(self, ctx, userRange=14):
        """
        Give a random password to the user
        """
        await ctx.send(secrets.token_urlsafe(userRange))

    """

    Events

    """
    """ Emoticons in text """
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
