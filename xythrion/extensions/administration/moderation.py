"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing as t

import discord
from discord.ext import commands as comms


class Moderation(comms.Cog):
    """Warning the user about specific actions taken.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(name='ban')
    async def hackban(self, ctx, user: t.Union[int, discord.Member], *,
                      reason: t.Optional[str] = None) -> None:
        """ """
        try:
            if isinstance(user, int):
                await ctx.guild.ban(discord.Object(id=user))

            elif isinstance(user, discord.Member):
                await ctx.guild.ban(user, reason=reason)

        except discord.Forbidden:
            raise comms.MissingPermissions


def setup(bot: comms.Bot) -> None:
    """The necessary function for loading in cogs within this file.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Moderation(bot))
