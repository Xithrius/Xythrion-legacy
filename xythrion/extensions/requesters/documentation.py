from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion


class Documentation(Cog):
    """Gets documentation for specific Python libraries."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("docs", "documentation"))
    async def fetch_documentation(self, ctx: Context, query: str) -> None:
        """Gets documentation of specific items for Python."""
        pass
