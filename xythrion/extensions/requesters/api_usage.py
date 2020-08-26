"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from typing import Optional

from discord import Embed
from discord.ext.commands import Cog, command, Context
from xythrion.bot import Xythrion


class APIUsage(Cog):
    """Changing permissions of guilds/users in different cases for usage of the bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is the owner of this bot."""
        return await self.bot.is_owner(ctx.author)

    @command(aliases=('guild_api_usage',))
    async def change_guild_api_usage(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Changes the way a guild interacts with the bots API usage."""
        guild = guild_id if guild_id else ctx.guild.id
        async with self.bot.pool.acquire() as conn:
            await conn.execute('INSERT INTO API_Usage(guild_id) VALUES ($1)', guild)

        await ctx.send(embed=Embed(description=f'Changed guild {guild} API permissions.'))

    @command(aliases=('user_api_usage',))
    async def change_user_api_usage(self, ctx: Context, user_id: Optional[int] = None) -> None:
        """Changes the way a user interacts with the bots API usage."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO Api_Usage(user_id) VALUES ($1)',
                user_id if user_id else ctx.author.id
            )

        await ctx.send(
            embed=Embed(description=f'Changed user {user_id if user_id else ctx.guild.id} API permissions.'))
