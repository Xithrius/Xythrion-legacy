from datetime import datetime
from typing import Optional, Union

import discord
from discord.ext.commands import Cog, Context, command
from humanize import naturaldelta

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, markdown_link


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

    @command(name='user', aliases=('userinfo',))
    async def _user(self, ctx: Context, member: Optional[Union[discord.Member, int]] = None) -> None:
        """Gets info of a user."""
        if isinstance(member, int):
            member = ctx.guild.get_member(member)

        elif isinstance(member, discord.Member):
            pass

        else:
            member = ctx.author

        d = {
            'User': [f'Username: {member.display_name}', f'Nickname: {member.nick}'],
            'Created on': [
                f'{member.created_at.strftime("%c")}, {naturaldelta(datetime.now() - member.created_at)}'],
            'Joined on': [
                f'{member.joined_at.strftime("%c")}, {naturaldelta(datetime.now() - member.joined_at)}']
        }

        formatted = '\n'.join([f'\n**{k}:**\n' + '\n'.join(x for x in v) for k, v in d.items()])
        embed = DefaultEmbed(description=formatted)

        embed.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)

    @command()
    async def server_icon(self, ctx: Context) -> None:
        """Shows the icon of a guild (server)."""
        embed = discord.Embed(description=markdown_link('icon url', ctx.guild.icon_url))

        embed.set_image(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
