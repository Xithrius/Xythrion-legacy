from random import choice, sample

import numpy as np
from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed


class Randoms(Cog):
    """Picking a bunch of different things at random (games based on random chance)."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("roll",))
    async def dice(self, ctx: Context, rolls: int = 1) -> None:
        """Rolls a die anywhere between 1 and 100."""
        if 1 < rolls < 100:
            s = round(np.sum(sample(range(1, 6), rolls)) / rolls, 3)
            msg = f"Die was rolled {rolls} time(s). Average output: {s}"
        else:
            msg = "Integer gives for rolls is invalid."

        embed = DefaultEmbed(ctx, description=msg)

        await ctx.send(embed=embed)

    @command(aliases=("pick",))
    async def choose(self, ctx: Context, *choices) -> None:
        """Returns only one of the items that the user gives."""
        embed = DefaultEmbed(ctx, description=f"A choice was made. Fate landed on {choice(choices)}.")
        await ctx.send(embed=embed)
