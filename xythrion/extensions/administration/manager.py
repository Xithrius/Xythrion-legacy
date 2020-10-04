from typing import Optional

from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed


class Manager(Cog, command_attrs=dict(hidden=True)):
    """Changing permissions of guilds/users in different cases for usage of the bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is the owner of this bot."""
        return await self.bot.is_owner(ctx.author)

    @command()
    async def restore_guild_api_permissions(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Restores the permissions for a specific guild."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                'DELETE FROM Blocked_Guilds WHERE guild_id = $1',
                guild_id if guild_id else ctx.guild.id
            )

        guild = self.bot.get_guild(guild_id) if not guild_id else ctx.guild
        embed = DefaultEmbed(
            ctx, description=f'API Permissions restored for guild "{guild.name if guild else guild_id}".')

        await ctx.send(embed=embed)

    @command()
    async def restore_user_api_permissions(self, ctx: Context, user_id: Optional[int] = None) -> None:
        """Restores API permissions for a user."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                'DELETE FROM Blocked_Users WHERE user_id = $1',
                user_id if user_id else ctx.author.id
            )

        user = self.bot.get_user(user_id) if user_id else ctx.author
        embed = DefaultEmbed(
            ctx, description=f'API Permissions restored for user {user.name if user else user_id}.')

        await ctx.send(embed=embed)

    @command()
    async def remove_guild_api_permissions(self, ctx: Context, guild_id: Optional[int] = None) -> None:
        """Removes API permissions for a specific guild."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO Blocked_Guilds(guild_id) VALUES ($1)',
                guild_id if guild_id else ctx.guild.id
            )

        guild = self.bot.get_guild(guild_id) if not guild_id else ctx.guild
        embed = DefaultEmbed(
            ctx, description=f'API Permissions removed from guild "{guild.name if guild else guild_id}".')

        await ctx.send(embed=embed)

    @command()
    async def remove_user_api_permissions(self, ctx: Context, user_id: Optional[int] = None) -> None:
        """Removes API permissions for a specific user."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO Blocked_Users(user_id) VALUES ($1)',
                user_id if user_id else ctx.author.id
            )

        user = self.bot.get_user(user_id) if user_id else ctx.author
        embed = DefaultEmbed(
            ctx, description=f'API Permissions Removed from user {user.name if user else user_id}.')

        await ctx.send(embed=embed)
