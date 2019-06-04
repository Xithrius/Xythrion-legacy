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


import random
import string

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now


# //////////////////////////////////////////////////////////////////////////// #
# Directives cog
# //////////////////////////////////////////////////////////////////////////// #
# A place for all general but simple commands to go
# //////////////////////////////////////////////////////////////////////////// #


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
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
    async def random_password(self, ctx, userRange):
        """
        Give a random password to the user
        """
        lst = [random.choice([string.ascii_letters, string.ascii_lowercase, string.ascii_uppercase]) for i in range(userRange)]
        await ctx.send(''.join(str(y) for y in lst))


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
