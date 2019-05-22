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


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
