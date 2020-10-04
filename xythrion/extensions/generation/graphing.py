import logging
import os
import re
from typing import List, Optional, Tuple, Union

import numpy as np
from discord.ext.commands import Cog, Context, Greedy, group
from sympy import symbols, sympify

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph

log = logging.getLogger(__name__)


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    # async def cog_check(self, ctx: Context) -> bool:
    #     """Checking if the user running commands is trusted by the owner."""
    #     return await self.bot.database.check_if_blocked(ctx)

    @staticmethod
    def create_graph_from_expression(
            ctx: Context, expression: str, domain: Optional[List[Union[int, float]]] = None) -> Graph:
        """
        Uses SymPy and MatPlotLib to create a graph from an expression.

        Dynamic numpy.arange by getting difference in domain and dividing by like 50.
        """
        # Removing the whitespace
        expression = re.sub(re.compile(r'\s+'), '', expression)

        # Creating the modifiable expression.
        expression = sympify(expression)

        # There will only be one variable.
        symbol = symbols('x')

        domain = domain if domain else (-10, 10)

        # Dynamic domain, 50 steps between domain numbers.
        x = np.arange(*domain, sum((abs(domain[0]), domain[1])) / 50)

        # Creating the y values.
        y = [expression.subs(symbol, i) for i in x]

        return Graph(ctx, x, y)

    @group(aliases=('plot',))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        pass

    @graph.command(aliases=('ex',))
    async def expression(self, ctx: Context, domain_nums: Greedy[Union[int, float]], *, expression: str
                         ) -> None:
        """
        Using SymPy and MatPlotLib to grab expressions that a user gives.

        Only supports single variable expressions.
        """
        if len(domain_nums) > 2:
            await ctx.send(embed=DefaultEmbed(
                ctx,
                description=f'Expected 2 domain numbers. Got {len(domain_nums)}: {domain_nums}'))
            return

        # async with ctx.typing():
        _graph = await self.bot.loop.run_in_executor(
            None, self.create_graph_from_expression, ctx, expression,
            domain_nums if len(domain_nums) else None)

        await ctx.send(file=_graph.embed.file, embed=_graph.embed)

        os.remove(_graph.save_path)

    @graph.command(enabled=False)
    async def points(self, ctx: Context, points: List[Tuple[Union[int, float]]]) -> None:
        """Graphing points on an x, y plane."""
        pass
