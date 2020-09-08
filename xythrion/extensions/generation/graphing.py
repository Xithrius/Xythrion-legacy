import os
from typing import Union

from discord.ext.commands import Cog, Context, Greedy, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, check_if_blocked, create_graph_from_expression


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is trusted by the owner."""
        return await check_if_blocked(ctx, self.bot.pool)

    @command()
    async def graph(self, ctx: Context, domain_nums: Greedy[Union[int, float]], *, expression: str) -> None:
        """
        Using SymPy and MatPlotLib to grab expressions that a user gives.

        Only supports single variable expressions.
        """
        if len(domain_nums) > 2:
            await ctx.send(embed=DefaultEmbed(
                description=f'Expected 2 domain numbers. Got {len(domain_nums)}: {domain_nums}'))
            return

        async with ctx.typing():
            f = await self.bot.loop.run_in_executor(None, create_graph_from_expression, expression,
                                                    domain_nums if len(domain_nums) else None)
            embed = DefaultEmbed(embed_attachment=f)

        await ctx.send(file=embed.file, embed=embed)

        os.remove(f)
