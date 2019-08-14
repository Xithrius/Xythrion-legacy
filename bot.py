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

from handlers.modules.output import path, printc


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=path('repository', 'logs', 'discord.log'), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Service_Connector:
    """ """

    def __init__(self, config):
        self.config = config
        self.services = {k: False for k in self.config.services._fields}

    async def start_services(self):
        await self.attempt_weather()
        await self.attempt_reddit()
        await self.attempt_osu()

    async def attempt_weather(self):
        f = self.config.services.weather
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code=12345&country=US&key={f}') as response:
                if response.status == 200:
                    if not self.services['weather']:
                        printc('[ ! ]: WEATHER SERVICE AVAILABLE')
                    self.services['weather'] = True
                else:
                    printc(f'WARNING: WEATHER SERVICE NOT AVAILABLE: {t.status}')

    async def attempt_reddit(self):
        f = self.config.services.reddit
        client_auth = aiohttp.BasicAuth(login=f.id, password=f.secret)
        post_data = {"grant_type": "password", "username": f.username, "password": f.password}
        headers = {"User-Agent": f"Xylene/{self.__version__} by {f.username}"}
        async with aiohttp.ClientSession(auth=client_auth, headers=headers) as session:
            async with session.post("https://www.reddit.com/api/v1/access_token", data=post_data) as response:
                if response.status == 200:
                    js = await response.json()
                    if not self.services['reddit']:
                        printc('[ ! ]: REDDIT SERVICE AVAILABLE')
                    self.services['reddit'] = {"Authorization": f"bearer {js['access_token']}", **headers}
                else:
                    printc(f'WARNING: REDDIT SERVICE NOT AVAILABLE: {t.status}')

    async def attempt_osu(self):
        f = self.config.services.osu
        parameters = {'k': f, 'u': 'Xithrius'}
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://osu.ppy.sh/api/get_user', params=parameters) as response:
                if response.status == 200:
                    if not self.services['osu']:
                        printc('[ ! ]: OSU! SERVICE AVAILABLE')
                    self.services['osu'] = True
                else:
                    printc(f'WARNING: OSU! SERVICE NOT AVAILABLE: {t.status}')


class Robot(comms.Bot, Service_Connector):
    """ """

    def __init__(self, *args, **kwargs):
        """ Objects:

        """
        super().__init__(*args, **kwargs)

        with open(path('handlers', 'configuration', 'config.json'), "r", encoding="utf8") as f:
            data = json.dumps(json.load(f))

        self.config = json.loads(data, object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

        self.__version__ = 'v0.0.1'

        Service_Connector.__init__(self, config=self.config)

        self.loop.create_task(self.load_services())

        self.owner_ids = set(self.config.owners)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name='the users')

        self.db_path = path('repository', 'data', 'requests.db')

        if not os.path.isfile(self.db_path):
            self.c = sqlite3.connect(self.db_path)
            c = self.c.cursor()
            services = ', '.join(str(y) for y in [f'{x} TEXT' for x in self.config.services._fields])
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
            self.c.commit()
            self.c.close()

    """ Background tasks """

    async def load_services(self):
        while not self.is_closed():
            await self.start_services()
            await asyncio.sleep(60)

    """ Events """

    async def on_ready(self):
        self.s = aiohttp.ClientSession()
        self.cog_folders = [folder for folder in os.listdir(path('cogs')) if folder != '__pycache__']
        self.exts = []
        for folder in self.cog_folders:
            folder_cogs = [f'cogs.{folder}.{cog[:-3]}' for cog in os.listdir(path('cogs', folder)) if os.path.isfile(path('cogs', folder, cog)) and cog[:-3] not in self.config.blocked_cogs]
            self.exts.extend(folder_cogs)
        printc('[. . .]: LOADING EXTENSIONS')
        for cog in self.exts:
            try:
                self.load_extension(cog)
            except Exception as e:
                printc(f'{cog}, {type(e).__name__}: {e}')
        printc('[ ! ]: BOT IS READY FOR USE')

    async def close(self):
        """ Safely closes connections """
        await self.s.close()
        try:
            self.c.close()
        except Exception as e:
            pass
        await super().close()

    """ Miscellaneous events """

    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        printc('[WARNING]: CLIENT HAS DISCONNECTED FROM NETWORK')

    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        # printc('[WARNING]: CLIENT HAS CONNECTED TO NETWORK')
        pass

    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        printc('[WARNING]: CLIENT HAS RESUMED CURRENT SESSION')


class MainCog(comms.Cog):
    """ """

    def __init__(self, bot):
        """ Objects:

        """
        self.bot = bot

    """ Cog checks """

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.owner_ids

    """ Commands """

    @comms.command()
    async def exit(self, ctx):
        """ Makes the bot log out """
        printc('[WARNING]: BOT IS LOGGING OUT')
        await ctx.bot.logout()

    @comms.command(name='r')
    async def reload(self, ctx):
        for cog in self.bot.exts:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except discord.ext.commands.errors.ExtensionNotFound:
                self.bot.exts.remove(cog)
        printc('[ ! ]: COGS HAVE BEEN RELOADED')
        await ctx.send(f'**{len(self.bot.exts)}** cog(s) have been reloaded', delete_after=30)

    @comms.command()
    async def list_cogs(self, ctx):
        await ctx.send(', '.join(str(y).split('.')[0] for y in self.bot.cogs.keys()))


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
