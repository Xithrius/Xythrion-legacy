"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from discord.ext.commands import Cog, command, Context, cooldown
from discord.ext.commands.cooldowns import BucketType
from xythrion.bot import Xythrion


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @cooldown(1, 5, BucketType.user)
    @command()
    async def graph(self, ctx: Context, *, entry: str) -> None:
        """Lexing then Graphing equations that the user gives."""
        pass
