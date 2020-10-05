from discord import Permissions
from discord.ext.commands import Cog, Context, command, group
from discord.utils import oauth_url

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, check_for_subcommands, markdown_link


class Links(Cog):
    """Links to many different things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checks if the user and/or guild has permissions for this command."""
        return await self.bot.database.check_if_blocked(ctx) and self.bot.database

    @command(aliases=('desc', 'description'))
    async def info(self, ctx: Context) -> None:
        """Information about bot origin along with usage statistics."""
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        embed = DefaultEmbed(
            ctx, title='**Links**', description='\n'.join(markdown_link(k, v) for k, v in info.items()))

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        url = oauth_url(self.bot.user.id, Permissions(19520))
        embed = DefaultEmbed(ctx, description=markdown_link('invite_link', url))

        await ctx.send(embed=embed)

    @group(aliases=('links',))
    async def link(self, ctx: Context) -> None:
        """Group command for management of links."""
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @link.command()
    async def show(self, ctx: Context, name: str) -> None:
        """Shows a link that a user selected."""
        pass

    @link.command()
    async def search(self, ctx: Context, name: str) -> None:
        """Queries the database for a link."""
        pass

    @link.command()
    async def random(self, ctx: Context) -> None:
        """Selects a random link from the database."""
        pass

    @link.command()
    async def add(self, ctx: Context, name: str, url: str) -> None:
        """Adds a link to the database."""
        pass

    @link.command()
    async def remove(self, ctx: Context, name: str) -> None:
        """Removes a link from the database."""
        pass
