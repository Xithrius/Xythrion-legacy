"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing
import datetime

from discord.ext import commands as comms
import discord


class Users(comms.Cog):
    """Moderating people in servers and bot commands."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.
        
        Returns:
            True or false based off of if user is an owner of the bot.
        
        """
        return await self.bot.is_owner(ctx.author)

    @comms.command()
    async def ignore(self, ctx, user: discord.User = None):
        pass

    @comms.command()
    async def unignore(self, ctx, user: typing.Union[discord.User, int] = None):
        pass


def setup(bot):
    bot.add_cog(Users(bot))
