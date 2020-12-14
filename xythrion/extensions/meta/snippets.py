from typing import Optional

from discord import Member
from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.utils import check_for_subcommands


class Snippets(Cog):
    """Storing blocks of code for later reference."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def snippet(self, ctx: Context) -> None:
        """Group command for code snippets."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @snippet.command()
    async def _list(self, ctx: Context, user: Optional[Member]) -> None:
        pass

    @snippet.command()
    async def _add(self, ctx: Context, name: str, content: str) -> None:
        pass

    @snippet.command()
    async def _remove(self, ctx: Context, name: str) -> None:
        pass
