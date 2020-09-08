from datetime import datetime
from logging import getLogger

from discord.ext.commands import Cog, Context, Greedy, command, is_owner
from humanize import naturaldate, precisedelta

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

log = getLogger(__name__)


class Dates(Cog):
    """Getting the time between dates."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command()
    @is_owner()
    async def create_date(self, ctx: Context, name: str, dates: Greedy[int]) -> None:
        """Creating a new data to track the time difference from."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Dates(t, id, name) Values($1, $2, $3)''',
                datetime(*dates), ctx.author.id, name
            )

        embed = DefaultEmbed(description=f'Date "{name}" has been put into the database.')

        await ctx.send(embed=embed)

    @command(name='date')
    async def _date(self, ctx: Context, name: str) -> None:
        """Getting the name of the date and the difference between now and then."""
        async with self.bot.pool.acquire() as conn:
            d = await conn.fetch('SELECT t FROM Dates WHERE name = $1', name)

        if len(d):
            delta = precisedelta(datetime.now() - d[0]["t"], minimum_unit='days', format='%0.4f',
                                 suppress=["months"])

            if datetime.now() > d[0]['t']:
                embed = DefaultEmbed(
                    description=f'{delta} have passed since {naturaldate(d[0]["t"])}, the start of "{name}".')

            else:
                embed = DefaultEmbed(description=f'{naturaldate(d[0]["t"])} is in {delta}.')

            await ctx.send(embed=embed)

        else:
            embed = DefaultEmbed(description=f'Could not find date named "{name}" stored in the database.')

            await ctx.send(embed=embed)
