"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info

The main file for the graphing bot.

Running the bot (python 3.8+):

    Installing requirements:
        $ python -m pip install --user -r requirements.txt

    Starting the bot:
        Without logging:
            $ python bot.py

        with logging (log should show up in /tmp/discord.log):
            $ python bot.py log
"""


import asyncio
import datetime
import json
import logging
import os
import sys
import traceback
from collections import defaultdict

import aiohttp
import asyncpg
import discord
from discord.ext import commands as comms
from hyper_status import Status

from modules import get_extensions, path


def _logger():
    """Logs information specifically for the discord package."""
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    if not os.path.isdir(path(f'tmp{os.sep}')):
        os.mkdir(path('tmp'))
    handler = logging.FileHandler(filename=path('tmp', 'discord.log'), encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(handler)


def _cleanup():
    """Cleans up tmp/ after bot is logged out and shut down."""
    if os.path.isdir(path('tmp')):
        for item in os.listdir(path('tmp')):
            if item[-4:] != '.log':
                os.remove(path('tmp', item))


class Xythrion(comms.Bot):
    """The main class where all important attributes are set and tasks are ran.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, *args, **kwargs):
        """Creating important attributes for this class.

        Args:
            Template: bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        super().__init__(*args, **kwargs)

        # Open config
        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)
        except (FileNotFoundError, IndexError):
            Status('Config could not be found or read properly.', 'fail')

        # Create asyncio loop
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.create_courtines())

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Getting cogs ready to be laoded in.
        __cogs = get_extensions()

        # Attempt to set TTS environment. If there's a failiure, the TTS cog isn't loaded.
        if os.path.isfile(path('config', 'gsc.json')):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('config', 'gsc.json')
        else:
            Status(
                'Google Service Token .json could not be opened properly. TTS is disabled.', 'fail')
            try:
                __cogs.remove('cogs.requesters.tts')
            except ValueError:
                pass

        # Loading the cogs in, one by one.
        for cog in __cogs:
            self.load_extension(cog)

        # Creating help dictionary for the help command.
        self.loop.run_until_complete(self.create_help())

    async def create_courtines(self):
        """Creates asynchronous database and session connection.

        Raises:
            Possible errors describing why connections could not be etablished.

        """
        try:
            self.pool = await asyncpg.create_pool(**self.config['db'], command_timeout=60)
            await self.check_database()
        except Exception as e:
            Status(f'Fatal error while creating connection to database: {e}', 'fail')

        self.session = aiohttp.ClientSession(loop=self.loop)

    async def check_database(self):
        """Checks if the database has the correct tables before starting the bot up."""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Runtime(
                    identification serial PRIMARY KEY,
                    t_login TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    t_logout TIMESTAMP WITHOUT TIME ZONE NOT NULL
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Ignore(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    id BIGINT,
                    reason TEXT
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Messages(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    id BIGINT,
                    jump TEXT
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Commands(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    id BIGINT,
                    jump TEXT,
                    command TEXT,
                    completed TIMESTAMP WITHOUT TIME ZONE
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Links(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    id BIGINT,
                    name TEXT,
                    link TEXT
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Dates(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    id BIGINT,
                    name TEXT
                )
            ''')

    async def create_help(self):
        """Creates multi-layer dictionary for helping users."""
        self.help_info = defaultdict(dict)

        for c in self.commands:
            h = c.help.split('\n')

            if not c.enabled or c.hidden:
                continue

            try:
                e = h[h.index('Command examples:') + 1:]
                examples = ', '.join(
                    str(y) for y in ["'{0}{1}'".format(self.command_prefix, x[x.index("]") + 1:]) for x in e]
                )

                self.help_info[c.cog.qualified_name][c.name.lower()] = {
                    'Aliases': ', '.join(str(y) for y in c.aliases) if c.aliases else 'None',
                    'Description': h[0], 'Examples': examples
                }
            except ValueError:
                Status(
                    f'Help setup error: docstring in cog {c.cog.qualified_name}: [prefix]{c.name}',
                    'fail'
                )

    async def on_ready(self):
        """Updates the bot status when logged in successfully."""
        self.startup_time = datetime.datetime.now()
        await self.change_presence(status=discord.ActivityType.playing,
                                   activity=discord.Game('with information'))
        Status('Awaiting...', 'ok')

    async def logout(self):
        """Subclassing the logout command to make sure connections are closed properly."""
        try:
            await self.session.close()
            await self.pool.close()
        except Exception:
            pass

        return await super().logout()


class Development(comms.Cog):
    """Cog required for development and control, along with some extras.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(aliases=['refresh', 'r'], hidden=True)
    async def reload(self, ctx):
        """Gets the cogs within folders and loads them into the bot after unloading current cogs.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Raises:
            Anything besides comms.ExtensionNotLoaded when loading cogs.

        Command examples:
            >>> [prefix]r
            >>> [prefix]refresh

        """
        for cog in get_extensions():
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            except Exception as e:
                Status(f'Loading "{cog}" error:', 'fail')
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

        # self.bot.loop.run_until_complete(self.bot.create_help())

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='loaded', hidden=True)
    async def loaded_extension(self, ctx):
        """Gives a list of the currently loaded cogs.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]loaded

        """
        lst = [f'{str(i).zfill(3)} | {k}' for i, k in enumerate(self.bot.cogs.keys())]
        c = '\n'.join(str(y) for y in lst)
        embed = discord.Embed(title='*Currently loaded cogs:*', description=f'```py\n{c}\n```')
        await ctx.send(embed=embed)

    @comms.command(hidden=True)
    async def exit(self, ctx):
        """Makes the bot logout after completing some last-second tasks.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]exit

        """
        try:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO Runtime(t_login, t_logout) VALUES($1, $2)''',
                    self.bot.startup_time, datetime.datetime.now())
        except AttributeError:
            pass
        Status('Logging out...', 'warn')
        await ctx.bot.logout()


if __name__ == "__main__":
    # Adding the temp folder if it doesn't exist.
    if not os.path.isdir(path('tmp')):
        os.mkdir(path('tmp'))

    # Starting the logger, if requested from the command line.
    try:
        if sys.argv[1] == 'log':
            _logger()
    except IndexError:
        pass

    # Creating the bot object
    bot = Xythrion(
        # command_prefix=comms.when_mentioned_or(';'),
        command_prefix=';',
        case_insensitive=True,
        help_command=None
    )

    # Running the bot
    try:
        bot.run(bot.config['discord'], bot=True, reconnect=True)
    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        Status('Improper token has been passed.', 'fail')

    # Cleaning up the tmp directory
    _cleanup()
