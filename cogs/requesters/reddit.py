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
    async def reddit(self, ctx, subreddit, status='hot', timeframe='day', amount: typing.Optional[int]=1):
        """Getting arguments from the user to make a Reddit request and giving an embed.
        
        Args:
            subreddit (str): The name of the subreddit.
            status (str): The current status of posts.
            timeframe (str): The interval which the subreddit posts should be picked from.
            amount (Optional[int]): An optional amount of posts from 1 to 10.

        Raises:
            AssertionError: Invalid parameters have been given to the command.
        
        """
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ['top', 'hot', 'controvertial', 'new', 'guilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if int(amount) not in range(1, 11):
            return await ctx.send(f'Please pick an amount of posts between 1 and 10')
        if status not in statuses:
            return await ctx.send(f'Please pick a status within `{", ".join(str(y) for y in statuses)}`')
        if timeframe not in timeframes:
            return await ctx.send(f'Please pick a timeframe within `{", ".join(str(y) for y in timeframes)}`')
        
        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, f'Status Code: {r.status}.'
            js = await r.json()
            js = js['data']['children']
            single = False

            if amount == 1:
                post = [js[random.randint(0, len(js))]['data']]
                if post[0]['url'][-4:] in ('.jpg', 'jpeg', '.png'):
                    single = post[0]['url'], post[0]['ups'], post[0]['author']
            else:
                pick = random.randint(0, len(js)) - amount
                post = [post['data'] for post in js[pick:pick + amount]]
            
            lst = [(shorten(item['title']), f"https://reddit.com{item['permalink']}") for item in post]
            embed = discord.Embed(title=f'*r/{subreddit}*',
                                  description='\n'.join(f'[`{y[0]}`]({y[1]})' for y in lst))
            if single:
                if single[0]:
                    embed.set_image(url=single[0])
                embed.set_footer(text=f'Upvotes: {single[1]}\nAuthor: u/{single[2]}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
