from discord.ext.commands import Cog, command

from xythrion import Context, Xythrion
from xythrion.utils import codeblock

HEADERS = {"Content-Type": "application/json"}
URL = "https://tinyy.io"


class Tinyy(Cog):
    """Shortening URLs with a simple API."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(aliases=("shorten_url", "shortener", "tinyy"))
    async def url_shortener(self, ctx: Context, url: str) -> None:
        """Shortening a URL provided by the user."""
        data = await self.bot.post(URL, json={"url": url}, headers=HEADERS)

        await ctx.embed(desc=codeblock(f"{URL}/{data['code']}"))
