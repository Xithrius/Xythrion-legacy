"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import collections
import json
import asyncpg
import asyncio
import aiohttp

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, get_cogs, ds


class Robot(comms.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=comms.when_mentioned_or('.'))

        self.loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_service_status())

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
