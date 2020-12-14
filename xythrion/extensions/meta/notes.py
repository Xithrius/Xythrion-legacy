from typing import Optional

from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.utils import check_for_subcommands


class Notes(Cog):
    """Keeping your notes organized in a bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def note(self, ctx: Context) -> None:
        """Group command for organizing notes."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @note.command()
    async def _list(self, ctx: Context) -> None:
        pass

    @note.command()
    async def _view(self, ctx: Context, name: str) -> None:
        pass

    @note.command()
    async def _add(self, ctx: Context, name: str, content: Optional[str] = None) -> None:
        pass

    @note.command()
    async def _remove(self, ctx: Context, name: str) -> None:
        pass

    @note.command()
    async def _append(self, ctx: Context, name: str, content: str) -> None:
        pass

    @note.command()
    async def _complete(self, ctx: Context, name: str, part: str) -> None:
        pass
