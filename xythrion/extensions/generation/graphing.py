import logging
import os
from pathlib import Path

import numpy as np
from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, gen_filename, parse

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.style.use('dark_background')

except Exception as e:
    log.critical(f'Error when importing matplotlib: {e}')


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def _create_graph(latex: str) -> str:
        """Creating the graph and then saving it to a file."""
        f = Path.cwd() / 'tmp' / f'{gen_filename()}.png'
        x = np.arange(-10, 10, 0.1)
        y = x

        plt.plot(x, y)

        plt.savefig(f)
        plt.clf()

        return str(f)

    @command()
    async def graph(self, ctx: Context, *, latex: str) -> None:
        """Lexing then Graphing equations that the user gives."""
        f = await self.bot.loop.run_in_executor(None, self._create_graph, latex)
        embed = DefaultEmbed(embed_attachment=f)

        await ctx.send(file=embed.file, embed=embed)

        os.remove(f)

    @command()
    async def tokenize(self, ctx: Context, *, ex: str) -> None:
        """Testing tokenization."""
        await ctx.send(parse(ex))
