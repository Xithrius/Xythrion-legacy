"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import discord
from discord.ext import commands as comms

from modules import describe_date, gen_block


class Dates(comms.Cog):
    """Fetching information about dates.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

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
    bot.add_cog(Dates(bot))
