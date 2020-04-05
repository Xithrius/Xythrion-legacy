"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

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

    """ Cog-specific checks """

    async def cog_check(self, ctx):
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    """ Commands """

    @comms.command(hidden=True)
    async def ignore(self, ctx, user_id: int, *, reason: str):
        """All commands to this bot by a specific user will be ignored.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user_id (int): The ID of the user to be ignored.

        Command examples:
            >>> [prefix]ignore 111111111111111111 Just a bit too toxic.

        """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Ignore(t, id, reason) VALUES ($1, $2, $3)''',
                datetime.now(), user_id, reason
            )

    @comms.command(hidden=True)
    async def unignore(self, ctx, user_id: int):
        """User will be removed from the database, and will be able to do commands again.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user_id (int): The ID of the user pardoned.

        Command examples:
            >>> [prefix]unignore 111111111111111111

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT reason FROM Ignore WHERE id = $1''',
                user_id
            )
            if len(info):
                await conn.execute(
                    '''DELETE FROM Ignore WHERE id = $1''',
                    user_id
                )
            else:
                await ctx.send(f'`User with ID {user_id} could not be found in the database.`')

    @comms.command(hidden=True)
    async def ban(self, ctx, user: int):
        """Bans a user from a guild (server).

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (int): The ID of the user to be banned.

        Command examples:
            >>> [prefix]ban 111111111111111111

        """
        try:
            await ctx.message.guild.ban(discord.Object(id=user))
            await ctx.send(f'<@{user}> with id {user} has been successfully banned.')
        except discord.Forbidden:
            await ctx.send('`This bot does not have enough permissions.`')

    @comms.command(hidden=True)
    async def kick(self, ctx, user: int):
        """Kicks a user from a guild (server).

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (int): The ID of the user to be kicked.

        Command examples:
            >>> [prefix]kick 111111111111111111

        """
        try:
            await ctx.message.guild.kick(discord.Object(id=user))
            await ctx.send(f'<@{user}> with id {user} has been successfully kicked.')
        except discord.Forbidden:
            await ctx.send('`This bot does not have enough permissions.`')


def setup(bot):
    bot.add_cog(Admin(bot))
