"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import discord
from discord.ext import commands as comms

from modules import gen_block, describe_date


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
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Commands(t, id, jump, command) VALUES ($1, $2, $3, $4)''',
                datetime.now(), ctx.author.id, ctx.message.jump_url, str(ctx.command)
            )

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

    @comms.command()
    async def since(self, ctx, *, name: str):
        """Tells you how long it has been since a date.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            name (str): The name of the date within the database.

        Command examples:
            >>> [prefix]since quarantine

        """
        async with self.bot.pool.acquire() as conn:
            d = await conn.fetch(
                '''SELECT t FROM Dates WHERE name = $1''', name
            )
            if len(d):
                delta = datetime.now() - d[0]['t']
                embed = discord.Embed(title=f'"{name}":')
                embed.description = gen_block([f'{describe_date(delta)} ago.'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'Could not find dated named "{name}"')

    @comms.command(hidden=True)
    @comms.is_owner()
    async def create_date(self, ctx, name, *, d: str = None):
        """Creates a date in the database to have the command 'since' calculate by.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            name (str): The name of the date within the database.
            d (str, optional): The date to be parsed, if any.

        Command examples:
            >>> [prefix]create_date
            >>> [prefix]create_date 2017 5 4

        """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Dates(t, id, name) VALUES ($1, $2, $3)''',
                datetime.now() if not d else datetime(*[int(x) for x in d.split()]),
                ctx.author.id, name
            )


def setup(bot):
    bot.add_cog(Records(bot))
