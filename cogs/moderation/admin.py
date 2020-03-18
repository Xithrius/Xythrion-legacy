"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from typing import Union

import discord
from discord.ext import commands as comms


class Admin(comms.Cog):
    """Summary for Admin

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command()
    async def ignore(self, ctx, user: discord.User = None):
        pass

    @comms.command()
    async def unignore(self, ctx, user: Union[discord.User, int] = None):
        pass


def setup(bot):
    bot.add_cog(Admin(bot))
