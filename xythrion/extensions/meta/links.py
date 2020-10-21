from discord import Permissions
from discord.ext.commands import Cog, Context, command
from discord.utils import oauth_url

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, markdown_link


class Links(Cog):
    """Links to many different things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @command(aliases=('desc', 'description'))
    async def info(self, ctx: Context) -> None:
        """Information about bot origin along with usage statistics."""
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        embed = DefaultEmbed(ctx, description='\n'.join(markdown_link(k, v) for k, v in info.items()))

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        url = oauth_url(self.bot.user.id, Permissions(19520))
        embed = DefaultEmbed(ctx, description=markdown_link('invite_link', url))

        await ctx.send(embed=embed)
