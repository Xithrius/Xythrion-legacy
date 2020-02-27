"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import aiohttp
import random
import typing

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import shorten


class Reddit(comms.Cog):
    """The Reddit cog that sends Reddit information in the form of an embed."""

    def __init__(self, bot):
        self.bot = bot

    @comms.cooldown(1, 5, BucketType.default)
    @comms.command(aliases=['sub', 'subreddit'])
    async def reddit(self, ctx, subreddit, status='hot', timeframe='day'):
        """Getting arguments from the user to make a Reddit request and giving an embed.
        
        Args:
            subreddit (str): The name of the subreddit.
            status (str): The current status of posts.
            timeframe (str): The interval which the subreddit posts should be picked from.

        Raises:
            AssertionError: Invalid parameters have been given to the command.
        
        """
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ['top', 'hot', 'controvertial', 'new', 'guilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if status not in statuses:
            return await ctx.send(f'Please pick a status within `{", ".join(str(y) for y in statuses)}`')
        if timeframe not in timeframes:
            return await ctx.send(f'Please pick a timeframe within `{", ".join(str(y) for y in timeframes)}`')
        
        lst = []
        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status
            js = await r.json()
            js = js['data']['children']
            p = js[random.randint(0, len(js))]['data']
            
            image = False
            if p['url'][-4:] in ('.jpg', 'jpeg', '.png'):
                image = p['url']

            embed = discord.Embed(title=f'*r/{subreddit}*', description=f'[`{shorten(p["title"])}`](https://reddit.com{p["permalink"]})')
            embed.set_footer(text=f'Upvotes: {p["ups"]}\nAuthor: u/{p["author"]}')
            if image:
                embed.set_image(url=image)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
