from discord.ext.commands import Cog

from xythrion.bot import Xythrion


class Vectorization(Cog):
    """Vector/matrix manipulation."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot
