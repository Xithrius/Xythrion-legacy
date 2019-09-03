"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    $ py -3 -m pip install --user -r requirements.txt
    $ py -3 bot.py

Todo:
    * Rewrite everything to match to PortgreSQL

"""


import collections
import json
import asyncpg
import asyncio

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, get_cogs, ds


class Robot(comms.Bot, Requesters):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=comms.when_mentioned_or('.'))

        self.loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_page(session, 'http://python.org'))

        #:

        #:
        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            data = json.load(f)

        #:
        self.config = json.loads(json.dumps(data), object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

    async def get_service_status(self):
        with aiohttp.ClientSession(loop=self.loop) as session:
            with aiohttp.Timeout(10):
                async with session.get(url) as response:
                    assert response.status == 200
                    print('got here')


class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    async def exit(self, ctx):
        await ctx.bot.logout()


if __name__ == "__main__":
    bot = Robot()
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
