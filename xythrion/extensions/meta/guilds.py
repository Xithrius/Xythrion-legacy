"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import discord
from discord.ext import commands as comms
from discord.ext.commands import Bot, Cog, Context

from xythrion.utils import markdown_link
from typing import Optional


class Guilds(Cog):
    """Getting information about guilds.

    Attributes:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command()
    async def icon(self, ctx: Context, mem: Optional[discord.Member] = None) -> None:
        """Shows the icon of a user.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.
            mem (:obj:`typing.Optional[discord.Member]`, optional): The user to get the icon url from.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]icon @Xithrius

        """
        mem = mem if mem else ctx.author

        embed = discord.Embed(description=markdown_link('icon url', mem.avatar_url))

        embed.set_image(url=mem.avatar_url)

        await ctx.send(embed=embed)

    @comms.command()
    async def server_icon(self, ctx: Context) -> None:
        """Shows the icon of a guild (server).

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]server_icon

        """
        embed = discord.Embed(description=markdown_link('icon url', ctx.guild.icon_url))

        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
