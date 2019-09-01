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
import os
import json
import sqlite3
import aiohttp
import asyncio
import logging

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, get_cogs, ds


class Robot(comms.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=comms.when_mentioned_or('.'))

        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            data = json.load(f)
        with open(path('handlers', 'configuration', 'urls.json'), 'r') as f:
            self.testing_urls = json.load(f)

        self.config = json.loads(json.dumps(data), object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))
        self.services = _data['services']
        self.requester_status = {x[:-3]: False for x in os.listdir(path('cogs', 'requesters')) if x[-3:] == '.py'}
        self.owner_ids = set(self.config.owners)
        self.req_p = path()
        self.rec_p = path()
        self.loop.create_task(self.load_services())

    async def load_services(self):
        while not self.is_closed():
            try:
                await self.s.close()
            except Exception as e:
                pass
            self.s = aiohttp.ClientSession()
            self.total_services = len(self.requester_status)
            self.broken_services = []
            for k, v in self.testing_urls.items():
                if k in self.config.blocked_cogs:
                    continue
                url = v['test_url']
                if 'TOKEN' in url:
                    url = url.replace('TOKEN', self.services[k])
                if 'headers' in v.keys():
                    headers = {k1: v1.replace('TOKEN', self.services[k]) for k1, v1 in v['headers'].items()}
                else:
                    headers = None
                try:
                    async with self.s.get(url, headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            self.requester_status[k] = True
                        else:
                            self.broken_services.append(f'[ {k.upper()} ]: {r.status} - {r}')
                except aiohttp.client_exceptions.ClientOSError:
                    pass
            await asyncio.sleep(60)

    async def on_ready(self):
        self.exts = get_cogs(self.config.blocked_cogs)
        broken_cogs = []
        ds('[. . .]: LOADING EXTENSIONS', '\r')
        for cog in self.exts:
            try:
                self.load_extension(cog)
            except Exception as e:
                broken_cogs.append(f'{cog}, {type(e).__name__}: {e}')
        if len(self.broken_services):
            errors = "\n\t".join(str(y) for y in self.broken_services)
            ds(f'[ WARNING ]: {len(self.broken_services)}/{self.total_services} SERVICE(S) BROKEN:\n{errors}')
        else:
            ds('[ SUCCESS ]: ALL EXTENSIONS AND SERVICES AVAILABLE', '\n')
        await self.change_presence(status=discord.ActivityType.playing, activity=discord.Game('with user data'))

    async def close(self):
        """Safely closes connections.

        Returns:
            Nothing. Bot should disconnect from the network no matter what when command is ran.

        """
        await self.s.close()
        await super().close()


class RecorderCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot
        if not os.path.isfile(self.bot.db_path):
            pass


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
