"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from typing import Optional, Union

import discord
from discord.ext import commands as comms
from discord.ext.commands import Cog, Bot, Context


class Moderation(Cog):
    """Warning the user about specific actions taken.

    Attributes:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(name='ban')
    @comms.has_permissions(ban_members=True)
    async def _ban(self, ctx: Context, user: Union[int, discord.Member], *,
                   reason: Optional[str] = None) -> None:
        """Bans a member either from their ID or a mention.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.
            user (:obj:`typing.Union[int, discord.Member]`):
                The member's ID or an object with their member attribtues from a mention.
            reason (:obj:`typing.Optional[str]`, optional): A reason for the punishment.

        Returns:
            :obj:`type(None)`: Always None

        Raises:
            :obj:`discord.ext.commands.MissingPermissions`:
                If the user execting the command does not have the correct permissions.

        Command examples:
            >>> [prefix]ban <@!111111111111111111> Unacceptable behavior.
            >>> [prefix]ban 111111111111111111 We do not allow that.

        """
        try:
            if isinstance(user, int):
                await ctx.guild.ban(discord.Object(id=user))

            elif isinstance(user, discord.Member):
                await ctx.guild.ban(user, reason=reason)

        except discord.Forbidden:
            raise comms.MissingPermissions
