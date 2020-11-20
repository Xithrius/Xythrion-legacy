from typing import Optional

from discord.ext import commands as comms

from xythrion.bot import Xythrion
from xythrion.constants import Config


class Source(comms.Cog):
    """Command to send the source (github repo) of a command."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @comms.command(name="source")
    async def send_source(self, ctx: comms.Context, arg1: Optional[str]) -> None:
        """Send the source GitGub url in an embed."""
        await ctx.send(Config.GITHUB_URL)  # for now
