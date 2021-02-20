import asyncio
import functools
import logging
import re
from tempfile import TemporaryFile
from typing import Any, Union

import numpy as np
from discord.ext.commands import Cog, Context, group
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph, check_for_subcommands, remove_whitespace

log = logging.getLogger(__name__)

ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")

TIMEOUT_FOR_GRAPHS = 10.0


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def calculate(expression: str) -> Any:
        """Calculate y-axis values from a set of x-axis values, given a math expression."""
        x = np.arange(-10, 10, 0.5)
        expr = parse_expr(expression)
        x_symbol = Symbol("x")

        y = np.array([expr.subs({x_symbol: x_point}).evalf(3) for x_point in x])

        return x, y

    def create_graph(self, ctx: Context, *graph_input: Union[str, Any]) -> DefaultEmbed:
        """Creates a graph object after getting values within a domain from an expression."""
        with TemporaryFile(suffix=".png") as buffer:
            x, y = self.calculate(graph_input) if isinstance(graph_input, str) else graph_input

            with Graph(ctx, buffer, x, y) as embed:
                return embed

    @group(aliases=("plot",))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command(aliases=("ex",))
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> None:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if "^" in expression:
            expression = expression.replace("^", "**")

        if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
            embed = DefaultEmbed(ctx, desc=f"Illegal character in expression: {illegal_char.group(0)}")
            await ctx.send(embed=embed)
            return

        else:
            func = functools.partial(self.create_graph, ctx, expression)
            future = self.bot.loop.run_in_executor(None, func)

            try:
                with ctx.typing():
                    embed = await asyncio.wait_for(future, TIMEOUT_FOR_GRAPHS, loop=self.bot.loop)
                    await ctx.send(file=embed.file, embed=embed)
            except asyncio.TimeoutError:
                embed = DefaultEmbed(ctx, desc=f"Timed out after {TIMEOUT_FOR_GRAPHS} seconds.")
                await ctx.send(embed=embed)

    @graph.command(aliases=("point",), enabled=False)
    async def points(self, ctx: Context, *, points: remove_whitespace) -> None:
        """
        Graphs points on a plot.

        Format: (x0, y0), (x1, y1), (x2, y2),... up to 10 points.
        """
        if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
            embed = DefaultEmbed(ctx, desc="Illegal character(s) in point array.")

            await ctx.send(embed=embed)

            return

        else:
            # *_ catches any other dimension of the array, so only 2d is captured.
            x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

            embed = await self.bot.loop.run_in_executor(None, self.create_graph, ctx, x, y)

            await ctx.send(file=embed.file, embed=embed)
