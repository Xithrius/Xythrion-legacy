import asyncio
import logging
from datetime import datetime

import aiohttp
from discord.ext.commands import Bot

from xythrion.databasing import Database

log = logging.getLogger(__name__)


class Xythrion(Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        # Setting the loop.
        self.loop = asyncio.get_event_loop()

        # Creating session for web requests.
        self.http_session = aiohttp.ClientSession()

        # Setting when the bot started up.
        self.startup_time = datetime.now()

        # Setting up the database.
        self.database = Database(self.loop)
        self.pool = self.database.pool

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.warning("Awaiting...")

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait_for(self.http_session.close(), 30.0, loop=self.loop)

        log.info("Finished up closing task(s): Closing http session.")

        return await super().logout()
