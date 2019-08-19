"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
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


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=path('repository', 'logs', 'discord.log'), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Robot(comms.Bot):
    """ Subclassing comms.Bot """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.s = aiohttp.ClientSession()

        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            data = json.dumps(json.load(f))

        with open(path('handlers', 'configuration', 'urls.json'), 'r') as f:
            self.testing_urls = json.load(f)

        self.config = json.loads(data, object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

        self.services = data['services']

        self.requester_status = {k: False for k in os.listdir(path('cogs', 'requesters')) if k[:-3] == '.py'}

        self.loop.create_task(self.load_services())

        self.owner_ids = set(self.config.owners)

        self.db_path = path('repository', 'data', 'requests.db')

        if not os.path.isfile(self.db_path):
            self.c = sqlite3.connect(self.db_path)
            c = self.c.cursor()
            services = ', '.join(str(y) for y in [f'{x} TEXT' for x in self.requester_status.keys()])
            c.execute(f'''CREATE TABLE Requests (id INTEGER, {services})''')
            c.execute('''CREATE TABLE Weather (id INTEGER,
                                               time INTEGER,
                                               high INTEGER,
                                               low INTEGER,
                                               humidity INTEGER,
                                               sunrise INTEGER,
                                               sunset INTEGER,
                                               moonrise INTEGER,
                                               moonset INTEGER,
                                               pop INTEGER,
                                               precip INTEGER,
                                               snow INTEGER,
                                               snow_depth INTEGER)''')
            c.execute('''CREATE TABLE Weather (id INTEGER,
                                               time INTEGER,
                                               high INTEGER,
                                               low INTEGER,
                                               humidity INTEGER,
                                               sunrise INTEGER,
                                               sunset INTEGER)''')
            self.c.commit()
            self.c.close()

    """ Background tasks """

    async def load_services(self):
        """ Calling services every minute """
        while not self.is_closed():
            await self.check_services()
            await asyncio.sleep(60)

    async def check_services(self):
        """ Checking availability of different services """
        for k, v in self.testing_urls.items():
            url = v['test_url']
            if 'TOKEN' in url:
                url.replace('TOKEN', self.services[k])
            if 'headers' in v.keys():
                headers = {k, v.replace('TOKEN', self.services[k]) for k, v in v['headers']}
            else:
                headers = None
            async with self.s.get(url, headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    if not self.requester_status[k]:
                        ds(f'[ SUCCESS ]: {k.upper()} SERVICE AVAILABLE')
                    self.requester_status[k] = True
                else:
                    ds(f'[ WARNING ]: {k.upper()} SERVICE NOT AVAILABLE: {r.status}')

    """ Events """

    async def on_ready(self):
        """ When ready, the session for requesting is loaded along with cogs """
        self.exts = get_cogs(self.config.blocked_cogs)
        ds('[. . .]: LOADING EXTENSIONS')
        for cog in self.exts:
            try:
                self.load_extension(cog)
            except Exception as e:
                ds(f'{cog}, {type(e).__name__}: {e}')
        ds('[ READY ]')
        game = discord.Game('the users')
        await self.change_presence(status=discord.ActivityType.watching, activity=game)

    async def close(self):
        """ Safely closes connections """
        await self.s.close()
        try:
            self.c.close()
        except Exception:
            pass
        await super().close()

    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        pass

    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        pass

    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        pass


class MainCog(comms.Cog):
    """ Essential cog for bugchecking """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks permissions of a user.

        Args:
            ctx: Context object where the command is called.

        Returns:
            True or false depending on if the user's id is in the owner set.

        """
        return ctx.author.id in self.bot.owner_ids

    """ Commands """

    @comms.command()
    async def exit(self, ctx):
        """Unloads currently loaded cogs, then loads from the 'cogs' directory.

        Args:
            ctx: Context object where the command is called.

        Raises:
            type(e).__name__: Cog cannot be loaded. Reason: 'e'.

        Returns:
            Errors, or a confirmation of success.

        """
        ds('[ WARNING ]: BOT IS LOGGING OUT')
        await ctx.bot.logout()

    @comms.command(name='r')
    async def reload(self, ctx):
        """Unloads currently loaded cogs, then loads from the 'cogs' directory.

        Args:
            ctx: Context object where the command is called.

        Raises:
            type(e).__name__: Cog cannot be loaded. Reason: 'e'.

        Returns:
            Errors, or a confirmation of success.

        """
        for cog in self.bot.exts:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                pass
        for cog in get_cogs(self.bot.config.blocked_cogs):
            try:
                self.bot.load_extension(cog)
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                pass
            except Exception as e:
                print(e)
        return ds('[ SUCCESS ]: COGS HAVE BEEN RELOADED')


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
