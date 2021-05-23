import asyncio
from datetime import datetime
from typing import Coroutine, Optional

import aiohttp
from discord import Message
from discord.ext import commands
from loguru import logger as log

from xythrion.context import Context


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        self.startup_time = datetime.now()

        self.http_session: Optional[aiohttp.ClientSession] = None

    async def get_context(self, message: Message, *, cls: commands.Context = Context) -> Coroutine:
        """Creating a custom context so new methods can be made for quality of life changes."""
        return await super().get_context(message, cls=cls)

    async def request(self, url: str, **kwargs) -> dict:
        """Requesting from a URl."""
        async with self.http_session.get(url, **kwargs) as response:
            assert response.status == 200, f"Could not request from URL. Status {response.status}."

            return await response.json()

    async def post(self, url: str, **kwargs) -> dict:
        """Posting to a URL."""
        async with self.http_session.post(url, **kwargs) as response:
            assert response.status == 200, f"Could not post to URL. Status {response.status}."

            return await response.json()

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.trace("Awaiting...")

    async def login(self, *args, **kwargs) -> None:
        """Creating all the important connections."""
        self.http_session = aiohttp.ClientSession()

        return await super().login(*args, **kwargs)

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.http_session.close()}, loop=self.loop, timeout=30.0)

        log.trace("Finished closing task(s).")

        return await super().logout()
