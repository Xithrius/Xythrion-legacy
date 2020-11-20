import os
from typing import List, Optional, Union

from discord import Message
from discord.ext.commands import Cog, Context, Greedy, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph, check_for_subcommands

UNSUPPORTED_CHARACTERS = ("!", "{", "}", "[", "]")


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group(aliases=("plot",), enabled=False)
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command()
    async def expression(
        self, ctx: Context, domain: Greedy[Union[int, float]], *, expression: str
    ) -> Optional[Message]:
        """
        Takes a single variable math expression and plots it.

        Supports any single variable, e, and pi. Factorials are not supported.
        """

        def create_graph(ex: str, domain_nums: Optional[List[Union[int, float]]]) -> Graph:
            """Creates a graph object after getting values within a domain from an expression."""
            pass

        if len(domain) != 2:
            embed = DefaultEmbed(ctx, desc=f"Expected 2 domain numbers. Got {len(domain)}: {domain}")
            return await ctx.send(embed=embed)

        illegal_characters = [char for char in UNSUPPORTED_CHARACTERS if char in expression]

        if any(illegal_characters):
            chars = ", ".join(illegal_characters)
            embed = DefaultEmbed(ctx, desc=f"Found unsupported characters in expression: {chars}")
            await ctx.send()

        domain = domain if len(domain) else None

        graph = await self.bot.loop.run_in_executor(None, create_graph, expression)

        await ctx.send(file=graph.embed.file, embed=graph.embed)

        os.remove(graph.save_path)
