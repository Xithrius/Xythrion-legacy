import numpy as np
from discord import Message
from discord.ext.commands import Cog

from xythrion.bot import Xythrion


MESSAGE_HISTORY_AMOUNT = 7
MAX_AVERAGE_TIME_DIFFERENCE = 0.3


class AntiCommandSpam(Cog):
    """Preventing the bot from being abused."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Checks if a user is spamming by calculating the time difference between messages.

        Time is averaged to see if the user is spamming very quickly.
        """
        messages = [
            msg.created_at
            for msg in await message.channel.history(limit=MESSAGE_HISTORY_AMOUNT)
            if msg.author == message.author
        ]

        avg = sum(np.diff(messages)) / MESSAGE_HISTORY_AMOUNT

        if avg < MAX_AVERAGE_TIME_DIFFERENCE:
            if await self.bot.database.check_if_blocked(message.author.id):
                async with self.bot.pool.acquire() as conn:
                    await conn.execute("INSERT INTO Blocked_Users(user_id) VALUES ($1)", message.author.id)
