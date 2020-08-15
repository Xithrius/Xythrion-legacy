"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
from datetime import datetime

import aiohttp
import discord
from discord.ext.commands import Bot
from logging import getLogger

log = getLogger(__name__)


class Xythrion(Bot):
    """A subclass where very important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Setting the loop.
        self.loop = asyncio.get_event_loop()

        # Creating the session for getting information from URLs by fetching with GETs.
        self.session = aiohttp.ClientSession()

    async def on_ready(self) -> None:
        """Updates the bot status when logged in successfully."""

        self.startup_time = datetime.now()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="graphs")
        )

        log.info('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        try:
            await asyncio.wait_for(self.session.close(), timeout=30.0, loop=self.loop)

        except asyncio.TimeoutError:
            log.critical(('Waiting for final tasks to complete timed out after 30 seconds.'
                          'Skipping, forcing logout'))

        log.info('Finished up closing tasks.')

        return await super().logout()
