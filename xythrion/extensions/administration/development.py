import time
from typing import Optional

from discord.ext.commands import Cog, ExtensionNotLoaded, command, is_owner
from loguru import logger as log

from xythrion.bot import Context, Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import Extension


class Development(Cog, command_attrs=dict(hidden=True)):
    """Cog required for development of this bot."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("refresh", "r"))
    @is_owner()
    async def reload(self, ctx: Context, *user_extensions: Optional[Extension]) -> None:
        """Reloads either all extensions or specific ones given by the user."""
        t0 = time.time()

        for extension in set(user_extensions or EXTENSIONS):
            try:
                self.bot.reload_extension(extension)

            except ExtensionNotLoaded:
                self.bot.load_extension(extension)

            except Exception as e:
                return log.error(f"Reloading {extension} error.", exc_info=(type(e), e, e.__traceback__))

        t1 = time.time()

        ms = (t1 - t0) * 1000

        if not user_extensions:
            msg = (
                f"Reloaded {len(self.bot.extensions)} extension(s) "
                f"containing {len(self.bot.cogs)} cog(s) in in about {ms}."
            )
        else:
            msg = f"Reloaded {len(user_extensions)} extension(s) in about {ms}."

        log.info(msg)

        await ctx.embed(desc=msg)
