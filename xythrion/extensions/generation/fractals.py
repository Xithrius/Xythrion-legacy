from typing import List, Union

from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion


class Fractals(Cog):
    """Creating fractals out of user inputs."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    def create_fractal(self, dimensions: List[Union[float, int]]) -> str:
        """Create the fractal image."""
        pass

    @command(name='fractal')
    async def _fractal(self, ctx: Context) -> None:
        """Giving a fractal to the user, with given inputs."""
        pass
