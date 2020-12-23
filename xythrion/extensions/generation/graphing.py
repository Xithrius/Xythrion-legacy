import re
from tempfile import TemporaryFile
from typing import List, Optional, Union

from discord import Message
from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, SimpleGraph, check_for_subcommands, remove_whitespace
from xythrion.utils.DSL import calculate

ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def create_graph(ctx: Context, x: List[Union[int, float]], y: List[Union[int, float]]) -> DefaultEmbed:
        """Creates a graph object after getting values within a domain from an expression."""
        # Interpreter stuffs
        with TemporaryFile(suffix=".png") as file:
            with SimpleGraph(ctx, x, y, file) as embed:
                return embed

    @group(aliases=("plot",))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command(aliases=("ex",))
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> Optional[Message]:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
            embed = DefaultEmbed(ctx, desc=f"Illegal character in expression: {illegal_char.group(0)}")
            return await ctx.send(embed=embed)

        x, y = calculate(expression)
        embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

        await ctx.send(file=embed.file, embed=embed)

    @graph.command(aliases=("point",))
    async def points(self, ctx: Context, *, points: remove_whitespace) -> Optional[Message]:
        """
        Graphs points on a plot.

        Format: (x0, y0), (x1, y1), (x2, y2),... up to 10 points.
        """
        if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
            embed = DefaultEmbed(ctx, desc="Illegal character(s) in point array.")
            return await ctx.send(embed=embed)

        x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

        embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

        await ctx.send(file=embed.file, embed=embed)
