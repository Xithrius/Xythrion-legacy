from discord import Permissions
from discord.ext.commands import Cog, command
from discord.utils import oauth_url

from xythrion.bot import Context, Xythrion
from xythrion.constants import Config
from xythrion.utils import markdown_link


class Links(Cog):
    """Links to many different things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command(aliases=("desc", "description"))
    async def info(self, ctx: Context) -> None:
        """Information about bot origin."""
        await ctx.embed(desc=markdown_link("Xythrion Github Repository", Config.GITHUB_URL))

    @command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        await ctx.embed(desc=markdown_link("invite_link", oauth_url(self.bot.user.id, Permissions(3525696))))
