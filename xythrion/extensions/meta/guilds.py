from typing import Optional

import discord
from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import markdown_link


class Guilds(Cog):
    """Getting information about guilds."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    async def icon(self, ctx: Context, mem: Optional[discord.Member] = None) -> None:
        """Shows the icon of a user."""
        mem = mem if mem else ctx.author

        embed = discord.Embed(description=markdown_link('icon url', mem.avatar_url))

        embed.set_image(url=mem.avatar_url)

        await ctx.send(embed=embed)

    @command()
    async def server_icon(self, ctx: Context) -> None:
        """Shows the icon of a guild (server)."""
        embed = discord.Embed(description=markdown_link('icon url', ctx.guild.icon_url))

        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
