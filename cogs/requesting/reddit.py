"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import random

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import shorten


class Reddit(comms.Cog):
    """The Reddit cog that sends Reddit information in the form of an embed.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Commands """

    @comms.cooldown(1, 5, BucketType.default)
    @comms.command(aliases=['sub', 'subreddit', 'r/'])
    async def reddit(self, ctx, subreddit: str, status: str = 'hot', timeframe: str = 'day'):
        """Requesting from the Reddit service to give a random post from a status within a timeframe.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            subreddit (str): The name of the subreddit.
            status (str): The current status of posts.
            timeframe (str): The interval which the subreddit posts should be picked from.

        Command examples:
            >>> [prefix]reddit pics top week
            >>> [prefix]sub pics

        """
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ['top', 'hot', 'controvertial', 'new', 'guilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if status not in statuses:
            return await ctx.send(f'Please pick a status within `{", ".join(str(y) for y in statuses)}`')
        if timeframe not in timeframes:
            return await ctx.send(f'Please pick a timeframe within `{", ".join(str(y) for y in timeframes)}`')

        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status
            js = await r.json()
            js = js['data']['children']
            p = js[random.randint(0, len(js) - 1)]['data']

            fail = False
            try:
                if p['over_18'] and not ctx.message.channel.is_nsfw():
                    fail = True
            except AttributeError:
                fail = True

            if fail:
                raise comms.CheckFailure(message='NSFW')

            image = False
            if p['url'][-4:] in ('.jpg', 'jpeg', '.png'):
                image = p['url']

            desc = f'[`{shorten(p["title"])}`](https://reddit.com{p["permalink"]})'
            embed = discord.Embed(title=f'*r/{subreddit}*',
                                  description=desc)
            embed.set_footer(text=f'Upvotes: {p["ups"]}\nAuthor: u/{p["author"]}')
            if image:
                embed.set_image(url=image)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
