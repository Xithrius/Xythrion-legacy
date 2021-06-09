from discord.ext.commands import Cog, group

from xythrion import Context, Xythrion
from xythrion.utils import and_join

BASE_URL = "https://api.warframestat.us"
PLATFORMS = ("pc", "ps4", "xb1", "swi")
PLANET_CYCLES = ("earth", "cetus")


class Warframe(Cog):
    """Getting information about the state of Warframe."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @group()
    async def warframe(self, ctx: Context) -> None:
        """The group command for information on the game of Warframe."""
        await ctx.check_for_subcommands()

    @warframe.command()
    async def state(self, ctx: Context, platform: str = "pc") -> None:
        """Getting world states from different planets."""
        if platform not in PLATFORMS:
            await ctx.embed(desc=f"Please pick a platform from the following: {and_join(PLATFORMS)}")

        data = await self.bot.request(f"{BASE_URL}/{platform}")

        planet_cycles = "\n".join(
            f"**{planet.title()}** - {data[planet + 'Cycle']['timeLeft']} remaining"
            for planet in PLANET_CYCLES
        )

        await ctx.embed(desc=planet_cycles)
