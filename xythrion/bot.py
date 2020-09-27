import asyncio
import logging
from datetime import datetime

import aiohttp
import asyncpg
from discord.ext.commands import Bot

from xythrion.constants import Postgresql
from xythrion.databasing import setup_database
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

        # Attempting to create the pool for asynchronous connections to the Postgresql database.
        try:
            self.pool = self.loop.run_until_complete(self.create_asyncpg_pool())
            log.info('Connected to Postgresql database successfully.')

            self.loop.run_until_complete(setup_database(self.pool))
            log.info('Setup database tables successfully.')

        except Exception as e:
            log.critical((
                'Could not create async connection pool and/or setup tables to/for Postgresql database. '
                f'Error: {e}'
            ))

    @staticmethod
    async def create_asyncpg_pool() -> asyncpg.pool.Pool:
        """Attempting to connect to the database."""
        return await asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60)

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.session.close(), self.pool.close()}, timeout=30.0, loop=self.loop)

        log.info('Finished up closing tasks.')

        return await super().logout()
