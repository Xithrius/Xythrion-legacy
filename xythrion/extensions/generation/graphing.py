import os
from typing import Union

from discord.ext.commands import Cog, Context, Greedy, group

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, Graph, check_for_subcommands


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group(aliases=('plot',))
    async def graph(self, ctx: Context) -> None:
        """Group function for graphing."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @graph.command(aliases=('ex',))
    async def expression(self, ctx: Context, domain_nums: Greedy[Union[int, float]], *, expression: str
                         ) -> None:
        """
        Using SymPy and MatPlotLib to grab expressions that a user gives.

        Only supports single variable expressions.
        """

        def create_graph_from_expression() -> Graph:
            """Creating graphs by parsing expressions through a tokenizer."""
            # domain = domain if domain else (-10, 10)

            # Dynamic domain, 50 steps between domain numbers.
            # x = np.arange(*domain, sum((abs(domain[0]), domain[1])) / 50)

            # Creating the y values.
            # y = np.array([expression.subs(symbol, i) for i in x])

            # return Graph(ctx, x, y)
            ...

        if len(domain_nums) > 2:
            await ctx.send(embed=DefaultEmbed(
                ctx,
                description=f'Expected 2 domain numbers. Got {len(domain_nums)}: {domain_nums}'))
            return

        # async with ctx.typing():
        _graph = await self.bot.loop.run_in_executor(
            None, create_graph_from_expression, expression, domain_nums if len(domain_nums) else None)

        await ctx.send(file=_graph.embed.file, embed=_graph.embed)

        os.remove(_graph.save_path)
