import asyncio
from datetime import datetime
from typing import Optional, Coroutine, Any

import aiohttp
from disnake import Message
from disnake.ext import commands
from loguru import logger as log

from bot.context import Context


class Xythrion(commands.Bot):
    """A subclass where important tasks and connections are created."""

    def __init__(self, *args, **kwargs) -> None:
        """Creating import attributes."""
        super().__init__(*args, **kwargs)

        self.startup_time = datetime.now()

        self.http_session: Optional[aiohttp.ClientSession] = None

        self.config = kwargs["config"]

        self.webserver_url = self.config["webserver"]["url"]

    async def get_context(self, message: Message, *, cls: Any = Context) -> Coroutine:
        """Overriding the base Context for this class."""
        return await super().get_context(message, cls=cls)

    @staticmethod
    async def on_ready() -> None:
        """Updates the bot status when logged in successfully."""
        log.info("Awaiting...")

    async def login(self, *args, **kwargs) -> None:
        """Creating all the important connections."""
        self.http_session = aiohttp.ClientSession()

        return await super().login(*args, **kwargs)

    async def close(self) -> None:
        """Subclassing the logout command to ensure connection(s) are closed properly."""
        await asyncio.wait(fs={self.http_session.close()}, loop=self.loop, timeout=30.0)

        log.info("Finished closing task(s).")

        return await super().close()
