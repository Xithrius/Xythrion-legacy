from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

HEADERS = {"Content-Type": "application/json"}
URL = "https://tinyy.io"


class Tinyy(Cog):
    """Shortening URLs with a simple API."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("shorten_url", "shortener", "tinyy"))
    async def url_shortener(self, ctx: Context, url: str) -> None:
        """Shortening a URL provided by the user."""
        async with self.bot.http_session.post(URL, json={"url": url}, headers=HEADERS) as resp:
            data = await resp.json()

        embed = DefaultEmbed(ctx, desc=f'```\n{URL}/{data["code"]}```')

        await ctx.send(embed=embed)
