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
    * More descriptive comments, maybe.

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


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class Robot(comms.Bot):
    """Subclassing comms.Bot to setup up all class attributes and services before cogs are loaded."""

    def __init__(self, *args, **kwargs):

        #: Initiating subclass with specific arg(s)/kwarg(s)
        super().__init__(command_prefix=comms.when_mentioned_or('.'))

        #: Opening config file to get settings and service details
        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            _data = json.load(f)
            data = json.dumps(_data)
        with open(path('handlers', 'configuration', 'urls.json'), 'r') as f:
            self.testing_urls = json.load(f)

        #: Giving attribute attributes of a named tuple
        self.config = json.loads(data, object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

        #: Attribute loading in service tokens (if any)
        self.services = _data['services']

        #: Dictionary created with the names of cogs in the requesters folder, while setting all values to false
        self.requester_status = {x[:-3]: False for x in os.listdir(path('cogs', 'requesters')) if x[-3:] == '.py'}

        #: Setting a set of owner ids that have owner access to the bot
        self.owner_ids = set(self.config.owners)

        #: Setting embed color once so it doesn't have to be repeated
        self.ec = 0xc27c0e

        #: Setting the database path for all cogs to use
        self.db_path = path('repository', 'data', 'requests.db')

        #: Creating background task for testing services
        self.loop.create_task(self.load_services())

        #: Checking if database exists. If database does not exist, tables are created for the requesters
        if not os.path.isfile(self.db_path):

            #: Building file and connecting to the empty database file
            self.c = sqlite3.connect(self.db_path)
            c = self.c.cursor()

            #: Building string of requester possibilities for users
            services = ', '.join(str(y) for y in [f'{x} TEXT' for x in self.requester_status.keys()])

            #: Adding requests and weather table to the database
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

            #: Closing database for now
            self.c.commit()
            self.c.close()

    """ Background tasks """

    async def create_timer(self):
        """Creating an instance of a timer to count up to a point, or keep track of time.

        Returns:
            An integer that builds up by 1 every second, starting at 0.

        """
        i = 0
        while not self.is_closed():
            await asyncio.sleep(1)
            i += 1
            return i

    async def load_services(self):
        """Calling services every minute to check if they're available for use.

        Returns:
            An error when a service is not available

        """
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
                try:
                    async with self.s.get(url, headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            self.requester_status[k] = True
                        else:
                            self.borked_services.append(f'[ {k.upper()} ]: {r.status} - {r}')
                except aiohttp.client_exceptions.ClientOSError:
                    pass
            await asyncio.sleep(60)

    """ Events """

    async def on_ready(self):
        """When the bot is ready cogs are loaded into the bot.

        Returns:
            Warnings if cogs and/or services aren't available

        """
        self.exts = get_cogs(self.config.blocked_cogs)
        borked_cogs = []
        ds('[. . .]: LOADING EXTENSIONS', '\r')
        for cog in self.exts:
            try:
                self.load_extension(cog)
            except Exception as e:
                borked_cogs.append(f'{cog}, {type(e).__name__}: {e}')
        if len(self.borked_services):
            errors = "\n\t".join(str(y) for y in self.borked_services)
            ds(f'[ WARNING ]: {len(self.borked_services)}/{self.total_services} SERVICE(S) BROKEN:\n{errors}')
        else:
            ds('[ SUCCESS ]: ALL EXTENSIONS AND SERVICES AVAILABLE', '\n')
        await self.change_presence(status=discord.ActivityType.playing, activity=discord.Game('with user data'))

    async def close(self):
        """Safely closes connections.

        Returns:
            Nothing. Bot should disconnect from the network no matter what when command is ran.

        """
        await self.s.close()
        try:
            self.c.close()
        except Exception:
            pass
        await super().close()

    async def on_disconnect(self):
        """Sends warning when the client disconnects from the network.

        Returns:
            Warning to the console if the timer has exceeded 10 seconds.

        """
        pass

    async def on_connect(self):
        """Sends warning when the client connects to the network.

        Returns:
            How long it took to reconnect, if it ever happened.

        """
        pass

    async def on_resumed(self):
        """Sends warning when the client resumes a session.

        Returns:
            If the client has connected but not resumed, another timer is started.

        """
        pass


class MainCog(comms.Cog):
    """The essential cog for bugchecking and refreshing the bot."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

        #: Creating help command
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        """Recreates help command if cog is unloaded

        Returns:
            A set help command depending on what's set in the class

        """
        self.bot.help_command = self._original_help_command

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

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot. It is not 'essential', but it's still useful.

        Args:
            ctx: Context object where the command is called.

        Returns:
            The invite link so the bot can be invited to a server.

        """
        await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=32885952')

    @comms.command()
    async def about(self, ctx):
        """Returns information about this bot's origin

        Args:
            ctx: Context object where the command is called.

        Returns:
            An embed object with links to creator's information and bot's repository.

        """
        info = {
            'Twitter': 'https://twitter.com/_Xithrius',
            'Github': 'https://github.com/Xithrius/Xythrion'
        }
        e = discord.Embed(title='Project creation date: March 30, 2019', description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()), colour=self.bot.ec)
        await ctx.send(embed=e)


if __name__ == "__main__":
    bot = Robot()
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
