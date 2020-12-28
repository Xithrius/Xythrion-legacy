import logging
import re
from tempfile import TemporaryFile
from typing import List, Optional, Union

from discord import Message
from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph, check_for_subcommands, remove_whitespace

log = logging.getLogger(__name__)

ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")

MATH_EXPRESSION_FORMAT = re.compile(r"(-?\d{1,5}(x\^(\.\d{1,5})?\+?)|x?)+")


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def create_graph(ctx: Context, x: List[Union[int, float]], y: List[Union[int, float]]) -> DefaultEmbed:
        """Creates a graph object after getting values within a domain from an expression."""
        # TODO: Interpreter stuffs
        with TemporaryFile(suffix=".png") as buffer:
            with Graph(ctx, buffer, x, y) as embed:
                return embed

    @group(aliases=("plot",))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command(aliases=("ex",), enabled=False)
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> Optional[Message]:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
            embed = DefaultEmbed(ctx, desc=f"Illegal character in expression: {illegal_char.group(0)}")
            return await ctx.send(embed=embed)

        if re.fullmatch(MATH_EXPRESSION_FORMAT, expression):
            ...

            # x, y = calculate(expression)
            # embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

            # await ctx.send(file=embed.file, embed=embed)

    @graph.command(aliases=("point",))
    async def points(self, ctx: Context, *, points: remove_whitespace) -> Optional[Message]:
        """
        Graphs points on a plot.

        Format: (x0, y0), (x1, y1), (x2, y2),... up to 10 points.
        """
        if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
            embed = DefaultEmbed(ctx, desc="Illegal character(s) in point array.")
            return await ctx.send(embed=embed)

        # *_ catches any other dimension of the array, so only 2d is captured.
        x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

        embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

        await ctx.send(file=embed.file, embed=embed)
