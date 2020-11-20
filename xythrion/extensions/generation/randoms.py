from random import randint

from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed


class Randoms(Cog):
    """Picking a bunch of different things at random (games based on random chance)."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("roll",))
    async def dice(self, ctx: Context, rolls: int = 1) -> None:
        """Rolls a die as many times as you want."""
        if rolls > 10 or rolls < 1:
            await ctx.send("`Rolls must be between 1 and 10.`")
            return

        elif rolls > 1:
            s = sum([randint(1, 6) for _ in range(rolls)]) / rolls
            avg = f"`Die was rolled {rolls} times. Average output: {round(s, 2)}`"

        else:
            avg = f"`Die was rolled once. Output: {randint(1, 6)}`"

        embed = DefaultEmbed(ctx, description=avg)

        await ctx.send(embed=embed)
