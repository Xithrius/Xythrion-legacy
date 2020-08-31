from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion


class Math(Cog):
    """Calculates equations and/or expressions."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=('calc',), enabled=False)
    async def calculate(self, ctx: Context, *, ex: str) -> None:
        """Parses and calculates the expression given by a user."""
        pass
