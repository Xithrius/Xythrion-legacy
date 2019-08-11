"""
>> Xylene
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

from handlers.modules.output import printc, path, now


class Osu_Requester(comms.Cog):
    """ Get information from WeatherBit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Aiohttp session
        Required headers for requests
        """
        self.bot = bot

    """ Events """

    @comms.Cog.listener()
    async def on_ready(self):
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        _owner = ctx.message.author.id in self.bot.owner_ids
        check = (_owner, self.h)
        return all(check)

    """ Commands """

    @comms.group()
    async def osu(self, ctx):
        """ """
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand is 'help':
            _help = [
                '.osu user <username>',
                '.osu beatmap <query>'
            ]
            _help = '\n'.join(str(y) for y in _help)
            await ctx.send(f'''**Help for the .reddit command**\n```\n{_help}```''')

    @osu.command()
    async def _user(self, ctx, **kwargs):
        await ctx.send(kwargs)


def setup(bot):
    bot.add_cog(Osu_Requester(bot))
