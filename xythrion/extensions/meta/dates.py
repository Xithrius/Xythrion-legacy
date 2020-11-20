from datetime import datetime

from discord.ext.commands import Cog, Context, Greedy, command
from humanize import naturaldate, precisedelta

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed


class Dates(Cog):
    """Getting the time between dates."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checks if the user and/or guild has permissions for this command."""
        return await self.bot.database.check_if_blocked(ctx) and self.bot.database

    @command()
    async def create_date(self, ctx: Context, name: str, dates: Greedy[int] = "now") -> None:
        """Creating a new data to track the time difference from."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO Dates(t, id, name) Values($1, $2, $3)""",
                datetime.now() if dates == "now" else datetime(*dates),
                ctx.author.id,
                name,
            )

        embed = DefaultEmbed(ctx, description=f'Date "{name}" has been put into the database.')

        await ctx.send(embed=embed)

    @command(name="date")
    async def date_info(self, ctx: Context, name: str) -> None:
        """Getting the name of the date and the difference between now and then."""
        async with self.bot.pool.acquire() as conn:
            d = await conn.fetch("SELECT t FROM Dates WHERE name = $1 AND id = $2", name, ctx.author.id)

        if len(d):
            delta = precisedelta(
                datetime.now() - d[0]["t"], minimum_unit="days", format="%0.4f", suppress=["months"]
            )

            if datetime.now() > d[0]["t"]:
                embed = DefaultEmbed(
                    ctx,
                    description=f'{delta} have passed since {naturaldate(d[0]["t"])}, the start of "{name}".',
                )

            else:
                embed = DefaultEmbed(ctx, description=f'{naturaldate(d[0]["t"])} is in {delta}.')

            await ctx.send(embed=embed)

        else:
            embed = DefaultEmbed(
                ctx, description=f'Could not find date named "{name}" stored in the database.'
            )

            await ctx.send(embed=embed)
