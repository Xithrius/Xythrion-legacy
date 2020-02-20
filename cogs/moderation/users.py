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

    @comms.command()
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
    async def cleanse(self, ctx, user: discord.User):
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch(
                '''SELECT identification FROM Punished WHERE identification=$1''',
                user.id)
            print(found)
            if len(found):
                await conn.execute(
                    '''DELETE FROM Punished WHERE identification=$1''',
                    user.id)
            else:
                await ctx.send(f'`User {user} with id {user.id} has been unignored.`')

    @comms.command()
    async def block_commands(self, ctx, user_id: int, *, reason: str):
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch(
                '''SELECT identification FROM Punished WHERE identification=$1''',
                user_id
            )
            if not len()


def setup(bot):
    bot.add_cog(Users(bot))
