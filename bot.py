"""
>> Xythrion
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

        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            _data = json.load(f)
            data = json.dumps(_data)

        with open(path('handlers', 'configuration', 'urls.json'), 'r') as f:
            self.testing_urls = json.load(f)

        self.config = json.loads(data, object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

        self.services = _data['services']

        self.requester_status = {x[:-3]: False for x in os.listdir(path('cogs', 'requesters')) if x[-3:] == '.py'}

        self.owner_ids = set(self.config.owners)

        self.db_path = path('repository', 'data', 'requests.db')

        self.loop.create_task(self.load_services())

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
            try:
                await self.s.close()
            except Exception as e:
                pass
            self.s = aiohttp.ClientSession()
            self.total_services = len(self.requester_status)
            self.borked_services = []
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
                async with self.s.get(url, headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        self.requester_status[k] = True
                    else:
                        self.borked_services.append(f'[ {k.upper()} ]: {r.status} - {r}')
            await asyncio.sleep(60)

    """ Events """

    async def on_ready(self):
        """ When ready, the session for requesting is loaded along with cogs """
        self.exts = get_cogs(self.config.blocked_cogs)
        borked_cogs = []
        ds('[. . .]: LOADING EXTENSIONS')
        for cog in self.exts:
            try:
                self.load_extension(cog)
            except Exception as e:
                borked_cogs.append(f'{cog}, {type(e).__name__}: {e}')
        if len(self.borked_services):
            errors = "\n\t".join(str(y) for y in self.borked_services)
            ds(f'[ WARNING ]: {len(self.borked_services)}/{self.total_services} SERVICE(S) BROKEN:\n{errors}')
        else:
            ds('[ READY ]: ALL SERVICES AND COGS')
        await self.change_presence(status=discord.ActivityType.watching, activity=discord.Game('the users'))

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
