import os
import re
from typing import List, Optional, Union

from discord import Message
from discord.ext.commands import Cog, Context, Greedy, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph, check_for_subcommands, remove_whitespace

ILLEGAL_CHARACTERS = re.compile(r"[!{}\[\]]+")


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def create_graph(
        domain_nums: Optional[List[Union[int, float]]], x: List[Union[int, float]], y: List[Union[int, float]]
    ) -> Graph:
        """Creates a graph object after getting values within a domain from an expression."""
        pass

    @group(aliases=("plot",))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command()
    async def points(self, ctx: Context, points: remove_whitespace) -> None:
        """
        Graphs points on a plot.

        Format: [(x0, y0), (x1, y1), (x2, y2),...] up to 100 points.
        """
        ...

    @graph.command()
    async def expression(
        self, ctx: Context, domain_numbers: Greedy[Union[int, float]], *, expression: remove_whitespace
    ) -> Optional[Message]:
        """
        Takes a single variable math expression and plots it.

        Supports one variable per expression (ex. x or y, not x and y), e, and pi.
        """
        if len(domain_numbers) not in (0, 2):
            return await ctx.send(
                f"There can be 2 or no domain integers/floats passed. {len(domain_numbers)} were passed."
            )

        if (illegal_char := re.search(ILLEGAL_CHARACTERS, expression)) is not None:
            embed = DefaultEmbed(ctx, desc=f"Illegal character in expression: {illegal_char.group(0)}")
            return await ctx.send(embed=embed)

        graph = await self.bot.loop.run_in_executor(None, self.create_graph, expression)

        await ctx.send(file=graph.embed.file, embed=graph.embed)

        os.remove(graph.save_path)
