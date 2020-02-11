"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import aiohttp
import random

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType


class Reddit(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    @comms.command(aliases=['sub', 'subreddit'])
    async def reddit(self, ctx, *, subreddit: str, status='hot', timeframe='day', posts: int=1):
        status, timeframe = status.lower(), timeframe.lower()
        statuses = ['top', 'hot', 'controvertial', 'new', 'guilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if int(posts) not in range(0, 20):
            return await ctx.send(f'Please pick a number of posts between 0 and 100')
        if status not in statuses:
            return await ctx.send(f'Please pick a status within {", ".join(str(y) for y in status)}')
        if timeframe not in timeframes:
            return await ctx.send(f'Please pick a status within {", ".join(str(y) for y in timeframes)}')
        
        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200
            js = await r.json()
            js = js['data']['children']
            try:
                if posts == 1:
                    post = js[random.randint(0, len(js))]['data']
                else:
                    pick = random.randint(0, len(js)) - posts
                    post = [post['data'] for post in js[pick:pick + posts]]
                lst = [(f"https://reddit.com{item['permalink']}", item['title']) for item in post]
                # NOTE: Make cut down function to shorten titles.
                embed = discord.Embed(description='\n'.join(f'[`{y[0]}`]({y[1]})' for y in lst))
            except IndexError:
                return await ctx.send(f'This subreddit does not have enough posts.')



def setup(bot):
    bot.add_cog(Reddit(bot))
