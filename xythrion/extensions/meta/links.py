from datetime import datetime
from typing import List

from discord import Embed, Permissions
from discord.ext.commands import Cog, Context, command, cooldown, group
from discord.ext.commands.cooldowns import BucketType
from discord.utils import oauth_url
from humanize import intcomma, naturaldelta

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, markdown_link


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

    @cooldown(1, 5, BucketType.user)
    @command(aliases=['uptime', 'runtime', 'desc', 'description'])
    async def info(self, ctx: Context) -> None:
        """Information about bot origin along with usage statistics."""
        media_links = await self.get_links()

        d = {
            'Links': media_links,
            'Lines of Python code': [intcomma(self.bot.line_amount)],
            'Current uptime': [naturaldelta(datetime.now() - self.bot.startup_time)]
        }
        formatted = '\n'.join([f'\n**{k}:**\n' + '\n'.join(x for x in v) for k, v in d.items()])
        embed = Embed(description=formatted)

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        url = oauth_url(self.bot.user.id, Permissions(19520))

        await ctx.send(embed=DefaultEmbed(single_url=('Invite url', url)))

    @group()
    async def link(self, ctx: Context, link_query: str) -> None:
        """Attempts to get a link from the database."""
        async with self.bot.pool.acquire() as conn:
            links = await conn.fetch('SELECT (name, link) FROM Links WHERE id = $1', ctx.author.id)
            if links:
                await ctx.send([x.link for x in links if x.name == link_query][0])

            else:
                embed = DefaultEmbed(description='No link by that name could be found.')
                await ctx.send(embed=embed)

    @link.command()
    async def create(self, ctx: Context, name: str, url: str) -> None:
        """Creates a link if it doesn't exist in the database."""
        async with self.bot.pool.acquire() as conn:
            links = await conn.fetch('SELECT * FROM Links WHERE name = $1', name)
            if len(links):
                embed = DefaultEmbed(description=f'Link "{name}" already exists in the database.')
                await ctx.send(embed=embed)

            else:
                await conn.execute(
                    'INSERT INTO Links(t, id, name, link) Values($1, $2, $3, $4)',
                    datetime.now(), ctx.author.id, name, url
                )

    @link.command()
    async def remove(self, ctx: Context, name: str) -> None:
        """Attempts to remove a link from the database."""
        async with self.bot.pool.acquire() as conn:
            await conn.execute('DELETE FROM Links WHERE id = $1, name = $2', ctx.author.id, name)
