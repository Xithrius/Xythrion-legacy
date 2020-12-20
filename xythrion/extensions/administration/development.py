from datetime import datetime
from logging import getLogger
from typing import Optional

import humanize
from discord.ext.commands import Cog, Context, ExtensionNotLoaded, command, is_owner

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import DefaultEmbed, Extension

log = getLogger(__name__)


class Development(Cog, command_attrs=dict(hidden=True)):
    """Cog required for development and control."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(name="reload", aliases=("refresh", "r"))
    @is_owner()
    async def reload(self, ctx: Context, *user_extensions: Optional[Extension]) -> None:
        """Reloads either all extensions or specific ones given by the user."""
        d = datetime.now()

        for extension in set(user_extensions or EXTENSIONS):
            try:
                self.bot.reload_extension(extension)

            except ExtensionNotLoaded:
                self.bot.load_extension(extension)

            except Exception as e:
                return log.error(f"Reloading {extension} error.", exc_info=(type(e), e, e.__traceback__))

        ms = humanize.naturaldelta(d - datetime.now(), minimum_unit="milliseconds")

        if not user_extensions:
            msg = (
                f"Reloaded {len(self.bot.extensions)} extension(s) "
                f"containing {len(self.bot.cogs)} cog(s) in in about {ms}."
            )
        else:
            msg = f"Reloaded {len(user_extensions)} extension(s) in about {ms}."

        log.info(msg)

        embed = DefaultEmbed(ctx, description=msg)

        await ctx.send(embed=embed)
