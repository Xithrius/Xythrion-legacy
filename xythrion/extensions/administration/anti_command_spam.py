import logging

import numpy as np
from discord import Message
from discord.ext.commands import Cog

from xythrion.bot import Xythrion

log = logging.getLogger(__name__)


class AntiCommandSpam(Cog):
    """Preventing the bot from being abused."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Checks if a user is spamming by calculating the time difference between messages."""
        messages = [
            msg.created_at
            for msg in await message.channel.history(limit=10).flatten()
            if msg.author == message.author
        ]
        log.trace(f"{np.diff(messages)}")
