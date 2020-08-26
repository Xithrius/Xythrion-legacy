"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from datetime import datetime
from typing import List

from discord import Embed
from discord.ext.commands import Cog, command, Context, cooldown
from discord.ext.commands.cooldowns import BucketType
from humanize import intcomma, naturaldate, naturaldelta
from xythrion.bot import Xythrion
from xythrion.utils import markdown_link


class Links(Cog):
    """Links to many different things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @staticmethod
    async def get_links() -> List[str]:
        """Provides links about the creator and bot."""
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        return [markdown_link(k, v) for k, v in info.items()]

    @staticmethod
    async def get_date_of_creation() -> List[str]:
        """Get the date between now and the day that this bot was created."""
        d = datetime(2019, 3, 13, 17, 16)

        return [f'{naturaldate(d)}; {naturaldelta(datetime.now() - d, months=False)} ago.']

    @cooldown(1, 5, BucketType.user)
    @command(aliases=['uptime', 'runtime', 'desc', 'description'])
    async def info(self, ctx: Context) -> None:
        """Information about bot origin along with usage statistics."""
        media_links = await self.get_links()
        project_length = await self.get_date_of_creation()

        d = {
            'Links:': media_links,
            'Lines of Python code:': intcomma(self.bot.line_amount),
            'Current uptime:': [naturaldelta(datetime.now() - self.bot.startup_time)],
            'Project length:': project_length
        }
        embed = Embed(description='\n'.join(markdown_link(k, v) for k, v in d.items()))

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        _id = self.bot.user.id
        permissions = {'Sending and reacting': 19520,
                       'Previous + removing messages': 27712,
                       'Administrator (not needed)': 8}
        url = f'https://discordapp.com/oauth2/authorize?client_id={_id}&scope=bot&permissions='
        invite_urls = {k: f'{url}{v}' for k, v in permissions.items()}
        invite_urls = '\n'.join(markdown_link(k, v) for k, v in invite_urls.items())

        embed = Embed(description='`Invite urls:`\n' + invite_urls)

        await ctx.send(embed=embed)

    @command(name='help', aliases=['h'])
    async def _help(self, ctx: Context) -> None:
        """Giving help to a user."""
        lst = [
            '`Help is most likely not ready yet, check the link just in case:`',
            markdown_link('Help with commands link', 'https://github.com/Xithrius/Xythrion#commands')
        ]

        embed = Embed(description='\n'.join(map(str, lst)))

        await ctx.send(embed=embed)

    @command(name='issue', aliases=['problem', 'issues'])
    async def _issue(self, ctx: Context) -> None:
        """Gives the user the place to report issues."""
        url = 'https://github.com/Xithrius/Xythrion/issues'
        embed = Embed(description=markdown_link('Report issue(s) here', url))

        await ctx.send(embed=embed)
