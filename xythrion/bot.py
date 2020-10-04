import asyncio
import logging
from datetime import datetime

import aiohttp
from discord.ext.commands import Bot

from xythrion.databasing import Database
from xythrion.utils import calculate_lines

log = logging.getLogger(__name__)


class Xythrion(Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        # Setting the loop.
        self.loop = asyncio.get_event_loop()

        # Creating session for web requests.
        self.session = aiohttp.ClientSession()

        # Setting when the bot started up.
        self.startup_time = datetime.now()

        # Counting the amount of lines within each Python file.
        self.line_amount = calculate_lines()

        # Setting up the database.
        self.pool = Database(self.loop).pool

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.warning('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.session.close(), self.pool.close()}, timeout=30.0, loop=self.loop)

        log.info('Finished up closing tasks.')

        return await super().logout()
