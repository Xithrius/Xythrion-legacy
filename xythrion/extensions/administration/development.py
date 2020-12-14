from datetime import datetime
from logging import getLogger
from typing import Optional

import humanize
from discord.ext.commands import Cog, Context, ExtensionNotLoaded, command, is_owner

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import DefaultEmbed

log = getLogger(__name__)


class Development(Cog, command_attrs=dict(hidden=True)):
    """Cog required for development and control."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(name="reload", aliases=("refresh", "r"))
    @is_owner()
    async def _reload(self, ctx: Context, ext: Optional[str] = None) -> None:
        """Reloads all extensions."""
        d = datetime.now()

        for extension in EXTENSIONS:
            try:
                self.bot.reload_extension(extension)

            except ExtensionNotLoaded:
                self.bot.load_extension(extension)

            except Exception as e:
                return log.warning(f"Reloading {extension} error: {e}")

        ms = humanize.naturaldelta(d - datetime.now(), minimum_unit="milliseconds")

        log.info(f'{ctx.author.name} reloaded extension{"" if ext else "s"} successfully in about {ms}.')

        embed = DefaultEmbed(
            ctx,
            description=f'Extension{" " + ext if ext else "s"} reloaded in about {ms}.',
        )

        await ctx.send(embed=embed)
