"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""

import discord
from discord.ext import commands as comms

from xythrion.utils import markdown_link
import typing as t


class Guilds(comms.Cog):
    """Getting information about guilds.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.
        guild_attributes (:obj:`t.List[str]`): All information ever wanted about a guild.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command()
    async def icon(self, ctx: comms.Context, mem: t.Optional[discord.Member] = None) -> None:
        """Shows the icon of a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            mem (:obj:`discord.Member`, optional): The user to get the icon url from.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]icon @Xithrius

        """
        mem = mem if mem else ctx.author

        embed = discord.Embed(description=markdown_link('icon url', mem.avatar_url))

        embed.set_image(url=mem.avatar_url)

        await ctx.send(embed=embed)

    @comms.command()
    async def server_icon(self, ctx: comms.Context) -> None:
        """Shows the icon of a guild (server).

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]server_icon

        """

        embed = discord.Embed(description=markdown_link('icon url', ctx.guild.icon_url))

        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot: comms.Bot) -> None:
    """The necessary function for loading in cogs within this file.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Guilds(bot))
