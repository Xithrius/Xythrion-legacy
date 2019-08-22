"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import json
import aiohttp
import random
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, now


class Reddit_Requester(comms.Cog):
    """ Getting information from Reddit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        return ctx.message.author.id in self.bot.owner_ids

    """ Commands """

    @comms.group()
    async def reddit(self, ctx):
        """ """
        if ctx.invoked_subcommand:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @reddit.command(name='top')
    async def _top(self, ctx, subreddit, amount=5):
        """ """
        async with self.bot.s.get('https://www.reddit.com/r/pics/top.json') as r:
            assert r.status == 200
            info = await r.json()
            info = info['data']['children']
            if 5 <= amount <= 25:
                info = info[:amount]
            if amount == 1:
                info = info[0]
            else:
                await ctx.send('Amount can only be in between 1 and 25')
                return

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command.cog_name == os.path.basename(__file__)[:-3] and type(error).__name__ == AssertionError:
            await ctx.send(f'Command **{ctx.command}** has failed at requesting information.')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
