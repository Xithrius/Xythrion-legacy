"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import asyncpg
import discord
from discord.ext import commands as comms

from modules import gen_block


class Records(comms.Cog):
    """Recording and outputting information based on users, by users.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Events """

    @comms.Cog.listener()
    async def on_message(self, message):
        """Records every single message sent by users for ranking.

        Args:
            message (discord.Message): Represents a message from Discord.

        """
        ctx = await self.bot.get_context(message)
        if not ctx.valid:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO Messages(t, id, jump) VALUES ($1, $2, $3)''',
                    message.created_at, message.author.id, message.jump_url
                )

    @comms.Cog.listener()
    async def on_command(self, ctx):
        """Records when a command is triggered.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        try:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO Commands(t, id, jump, command) VALUES ($1, $2, $3, $4)''',
                    datetime.now(), ctx.author.id, ctx.message.jump_url, str(ctx.command)
                )

        except asyncpg.exceptions._base.InterfaceError:
            pass

    @comms.Cog.listener()
    async def on_command_completion(self, ctx):
        """Records in the same place as the event 'on_command', but when the command is completed.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''UPDATE Commands SET completed=$2 WHERE jump=$1''',
                ctx.message.jump_url, datetime.now()
            )

    """ Commands """

    @comms.command()
    async def rank(self, ctx, user: discord.User = None):
        """Gets rank information about the user.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (discord.User): The user that will have their information retrieved (defaulted to None).

        Command examples:
            >>> [prefix]rank @Xithrius
            >>> [prefix]rank

        """
        user = user if user is not None else ctx.author
        async with self.bot.pool.acquire() as conn:
            messages = await conn.fetch(
                '''SELECT jump FROM Messages WHERE id = $1''',
                user.id
            )
            commands = await conn.fetch(
                '''SELECT jump FROM Commands WHERE id = $1''',
                user.id
            )
        embed = discord.Embed(title=f'***Calculated rank for {user.name}:***')
        desc_lst = [
            f'Total commands executed: {len(commands)}',
            f'Total messages: {len(messages)}'
        ]
        embed.description = gen_block(desc_lst)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Records(bot))
