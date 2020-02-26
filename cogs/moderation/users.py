"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncpg
import datetime

from discord.ext import commands as comms
import discord


class Users(comms.Cog):
    """Moderating people in servers and bot commands."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.
        
        Returns:
            True or false based off of if user is an owner of the bot.
        
        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(enabled=False)
    async def punish(self, ctx, user: discord.User, *, reason: str):
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch(
                '''SELECT identification from Punished WHERE identification=$1''',
                user.id)
            if not len(found):
                await conn.execute(
                    '''INSERT INTO Punished(identification, reason, time) VALUES ($1, $2, $3)''',
                    ctx.message.author.id, reason, datetime.datetime.now())
                await ctx.send(f'`User {user} with id {user.id} has successfully been ignored for most/all interactions with this bot.`')
            else:
                await ctx.send('`User has already been ignored.`')

    @comms.command()
    async def ignore(self, ctx, user_id: int, *, reason: str):
        """ """
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch('''SELECT identification FROM Users WHERE identification=$1,''',
                                     user_id
            )
            print(found)
            # if len(found):

    @comms.command()
    async def unignore(self, ctx, user_id: int):
        """ """
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch('''SELECT identification FROM Users WHERE identification=$1,''',
                                     user_id
            )


def setup(bot):
    bot.add_cog(Users(bot))
