"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from typing import List, Union

from discord.ext.commands import Cog, command, Context
from xythrion.bot import Xythrion
from xythrion.utils import parallel_executor


class Fractals(Cog):
    """Creating fractals out of user inputs."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @parallel_executor
    def create_fractal(self, dimensions: List[Union[float, int]]) -> str:
        """Create the fractal image."""
        pass

    @command(name='fractal')
    async def _fractal(self, ctx: Context) -> None:
        """Giving a fractal to the user, with given inputs."""
        pass
