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

    @comms.group()
    @comms.cooldown(1, 60, BucketType.default)
    async def reddit(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Possible reddit commands: `u` and `r`')

    @reddit.command(aliases=['sub', 'subreddit'])
    async def r(self, ctx, *, subreddit: str, status='hot', timeframe='day'):
        statuses = ['top', 'hot', 'controvertial', 'new', 'guilded']
        timeframes = ['hour', 'day', 'week', 'month', 'year', 'all']

        if status not in statuses:
            await ctx.send(f'Please pick a status within {", ".join(str(y) for y in status)}')
        if timeframe not in timeframes:
            await ctx.send(f'Please pick a status within {", ".join(str(y) for y in timeframes)}')
        url = f'https://reddit.com/r/{subreddit}/{status}.json?limit=100&t={timeframe}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200
            js = await r.json()

    @reddit.command(aliases=['user'])
    async def u(self, ctx, *, user: str):
        pass


def setup(bot):
    bot.add_cog(Reddit(bot))
