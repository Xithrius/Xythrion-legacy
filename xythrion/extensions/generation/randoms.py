from collections import Counter
from random import randint

import pandas as pd
from discord.ext.commands import Cog, command

from xythrion import Context, Xythrion
from xythrion.utils import graph_2d


class Randoms(Cog):
    """Picking a bunch of different things at random (games based on random chance)."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("roll",))
    async def dice(self, ctx: Context, rolls: int = 1) -> None:
        """Rolls a die anywhere between 1 and 10 times."""
        if rolls not in range(1, 11):
            return await ctx.embed(desc="Amount of rolls must be between 1 and 10.")

        counts = Counter(randint(1, 6) for _ in range(rolls))

        df = pd.DataFrame([[i, counts[i]] for i in range(1, 7)], columns=("roll", "amount"))

        buffer = await graph_2d(
            df["roll"],
            df["amount"],
            graph_type="bar",
            autorotate_xaxis=False
        )

        await ctx.embed(
            desc=f"Graph of {rolls} dice roll{'s' if rolls > 1 else ''}.",
            buffer=buffer
        )
