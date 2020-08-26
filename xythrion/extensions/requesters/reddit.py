"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from random import randint

from discord import Embed, Message
from discord.ext.commands import CheckFailure, Cog, command, Context
from xythrion.bot import Xythrion
from xythrion.utils import shorten


class Reddit(Cog):
    """The Reddit cog that sends Reddit information in the form of an embed."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Scans for Reddit posts and provides info on them."""
        pass

    @command(aliases=['sub', 'subreddit'])
    async def reddit(self, ctx: Context, subreddit: str, status: str = 'hot', timeframe: str = 'day') -> None:
        """Requesting from the Reddit service to give a random post from a status within a timeframe."""
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ['top', 'hot', 'controversial', 'new', 'gilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if status not in statuses:
            await ctx.send(f'Please pick a status within `{", ".join(str(y) for y in statuses)}`')

        if timeframe not in timeframes:
            await ctx.send(f'Please pick a timeframe within `{", ".join(str(y) for y in timeframes)}`')

        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'

        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status

            js = await r.json()
            js = js['data']['children']
            p = js[randint(0, len(js) - 1)]['data']

            fail = False

            try:
                if p['over_18'] and not ctx.message.channel.is_nsfw():
                    fail = True

            except AttributeError:
                fail = True

            if fail:
                raise CheckFailure(message='NSFW')

            image = False

            if p['url'][-4:] in ('.jpg', 'jpeg', '.png'):
                image = p['url']

            desc = f'[`{shorten(p["title"])}`](https://reddit.com{p["permalink"]})'
            embed = Embed(title=f'*r/{subreddit}*', description=desc)

            embed.set_footer(text=f'Upvotes: {p["ups"]}\nAuthor: u/{p["author"]}')

            embed.set_image(url=image if image else '')

            await ctx.send(embed=embed)
