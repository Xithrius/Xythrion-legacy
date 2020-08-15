"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands import Cog, Context
from discord.ext.commands.cooldowns import BucketType

from xythrion.bot import Xythrion


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command(enabled=False)
    async def graph(self, ctx: Context, *, entry: str) -> None:
        """Lexing then Graphing equations that the user gives."""
        # NOTE: Will be filled in once lexer utility is finished.
        pass
