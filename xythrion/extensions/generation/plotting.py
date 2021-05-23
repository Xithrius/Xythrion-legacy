import asyncio
import logging
import re
from typing import Union

import numpy as np
from discord.ext.commands import Cog, group
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr

from xythrion import Context, Xythrion
from xythrion.utils import graph_2d, remove_whitespace

log = logging.getLogger(__name__)

ILLEGAL_EXPRESSION_CHARACTERS = re.compile(r"[!{}\[\]]+")
POINT_ARRAY_FORMAT = re.compile(r"(-?\d+(\.\d+)?),(-?\d(\.\d+)?)")

TIMEOUT_FOR_GRAPHS = 10.0


class Plotting(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def calculate(expression: str, bounds: Union[int, float] = 10) -> tuple[np.ndarray, np.ndarray]:
        """Calculate y-axis values from a set of x-axis values, given a math expression."""
        bounds = abs(bounds)
        x = np.arange(-bounds, bounds, bounds / 50)
        expr = parse_expr(expression)
        x_symbol = Symbol("x")

        y = np.array([expr.subs({x_symbol: x_point}).evalf() for x_point in x])

        return x, y

    @group(aliases=("graph",))
    async def plot(self, ctx: Context) -> None:
        """Group function for graphing."""
        await ctx.check_for_subcommands()

    @plot.command(aliases=("ex",))
    async def expression(self, ctx: Context, *, expression: remove_whitespace) -> None:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if "^" in expression:
            expression = expression.replace("^", "**")

        if (illegal_char := re.search(ILLEGAL_EXPRESSION_CHARACTERS, expression)) is not None:
            return await ctx.embed(desc=f"Illegal character in expression: {illegal_char.group(0)}")

        future = self.bot.loop.run_in_executor(None, self.create_graph, ctx, expression)

        try:
            with ctx.typing():
                embed = await asyncio.wait_for(future, TIMEOUT_FOR_GRAPHS, loop=self.bot.loop)

                await ctx.send(file=embed.file, embed=embed)

        except asyncio.TimeoutError:
            await ctx.embed(desc=f"Timed out after {TIMEOUT_FOR_GRAPHS} seconds.")

    @plot.command(aliases=("point",), enabled=False)
    async def points(self, ctx: Context, *, points: remove_whitespace) -> None:
        """
        Plots points on a plot.

        Format: (x0, y0), (x1, y1), (x2, y2),...
        """
        if not (point_array := re.finditer(POINT_ARRAY_FORMAT, points)):
            return await ctx.embed(desc="Illegal character(s) in point array.")

        # *_ catches any other dimension of the array, so only 2d is captured.
        x, y, *_ = zip(*[list(map(float, point.group(0).split(","))) for point in point_array])

        embed = await graph_2d(x, y)

        await ctx.send(file=embed.file, embed=embed)
