"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info

Running the bot:

    Make sure your Python version is 3.7.x:
        Windows:
            $ py -3.7 -V

        Linux/OSX:
            $ python3 -V

    If not, install Python version 3.7.7:
        https://python.org/download

    Creating the virtual environment (defaulting to "python", replace if needed):
        NOTE: DO NOT INCLUDE "pip" YOU'RE RUNNING THIS ON UBUNTU.
        $ python -m pip install --upgrade pip virtualenv

        # Creating the virtual environment, then activating it.
        $ python -m virtualenv venv
        $ source venv/Scripts/activate

    Installing requirements:
        $ python -m pip install --user -r requirements.txt

    Running the bot:
        Windows:
            $ py -3.7 bot.py

        Linux/OSX:
            $ clear && python3 bot.py

"""


import asyncio
import concurrent.futures
import datetime
import json
import logging
import os
import sys
import traceback
import typing as t

import aiohttp
import asyncpg
import discord
from discord.ext import commands as comms
from rich import logging as r_logging, r_traceback

from utils import markdown_link, path, tracebacker


try:
    r_traceback.install()

except Exception as e:
    tracebacker(e)


def _discord_logger() -> None:
    """Logs information specifically for the discord package."""
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    if not os.path.isdir(path(f'tmp{os.sep}')):
        os.mkdir(path('tmp'))

    base_handler = logging.FileHandler(filename=path('tmp', 'discord.log'), encoding='utf-8', mode='w')
    base_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(base_handler)


def _rich_logger(log_type: t.Union[str, bool]) -> logging.Logger:
    log_types = {'info': logging.INFO, 'debug': logging.DEBUG, None: 'NOTSET'}[log_type]

    # _format = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    logging.basicConfig(
        level=log_types, format='%(message)s', datefmt="[%c]", handlers=[r_logging.RichHandler()]
    )

    return logging.getLogger('rich')


def _cleanup() -> None:
    """Cleans up tmp/ after bot is logged out and shut down."""
    if os.path.isdir(path('tmp')):
        for item in os.listdir(path('tmp')):
            if item[-4:] != '.log':
                os.remove(path('tmp', item))


class Xythrion(comms.Bot):
    """A subclass where very important tasks and connections are created.

    Attributes:
        config (dict): Tokens and other items from `./config/config.json`.
        loop (:obj:`asyncio.AbstractEventLoop`):
        pool (:obj:`asyncpg.Pool`):
        session (:obj:``):

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of tasks and connections."""
        self.log = kwargs.pop('log')

        super().__init__(*args, **kwargs)

        # Open config
        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)

        except IndexError:
            pass

        except FileNotFoundError:
            pass

        # Create asyncio loop
        self.loop = asyncio.get_event_loop()

        # Create executor for running sync functions asynchronously
        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.loop.run_until_complete(self.create_courtines())

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Loading the cogs in, one by one.
        asyncio.get_event_loop().run_until_complete(self.load_extensions())

        # Creating help dictionary for the help command.
        # asyncio.get_event_loop().run_until_complete(self.create_help())

    async def create_courtines(self) -> None:
        """Creates asynchronous database and session connection.

        Raises:
            Possible errors describing why connections could not be etablished.

        """
        try:
            self.pool = await asyncpg.create_pool(**self.config['db'], command_timeout=60)
            await self.check_database()

        except Exception as e:
            self.log.info(f'Fatal error while creating connection to database: {e}')

        self.session = aiohttp.ClientSession()

    async def check_database(self) -> None:
        """Checks if the database has the correct tables before starting the bot up."""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Runtime(
                    identification serial PRIMARY KEY,
                    t_login TIMESTAMP WITH TIME ZONE NOT NULL,
                    t_logout TIMESTAMP WITH TIME ZONE NOT NULL
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS FailedCommands(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITH TIME ZONE NOT NULL,
                    id BIGINT,
                    jump TEXT,
                    error TEXT
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS ReportedIssues(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITH TIME ZONE NOT NULL,
                    id BIGINT,
                    flag TEXT,
                    content TEXT
                )
            ''')

    async def load_extensions(self) -> None:
        """ """
        extensions = await self.get_extensions()
        broken_extensions = []

        for extension in extensions:
            try:
                self.load_extension(extension)

            except Exception as e:
                broken_extensions.append((extension, e))

        for extension, error in broken_extensions:
            tracebacker(error)

    async def get_extensions(self) -> t.List[str]:
        extensions = []

        for folder in os.listdir(path('cogs')):
            extensions.extend(
                [f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py']
            )

        return extensions

    async def on_ready(self) -> None:
        """Updates the bot status when logged in successfully."""
        await self.wait_until_ready()

        self.startup_time = datetime.datetime.now()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="graphs")
        )

        self.log.info('Awaiting...')

    async def logout(self) -> None:
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

    def __init__(self, bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    async def cog_check(self, ctx) -> None:
        """Checks if user if owner.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    async def _reload(self, ctx) -> None:
        """Gets the cogs within folders and loads them into the bot after unloading current cogs.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Raises:
            Anything besides comms.ExtensionNotLoaded when loading cogs.

        Command examples:
            >>> [prefix]r
            >>> [prefix]refresh

        """
        for cog in await self.get_extensions():
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            except Exception as e:
                self.log.info(f'Loading "{cog}" error:')
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='loaded', hidden=True)
    async def _loaded_extensions(self, ctx: comms.Context) -> None:
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

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    async def _exit(self, ctx: comms.Context) -> None:
        """Makes the bot logout after completing some last-second tasks.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]exit

        """
        try:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO Runtime(t_login, t_logout) VALUES($1, $2)''',
                    self.bot.startup_time, datetime.datetime.now()
                )

        except AttributeError:
            pass

        self.bot.log.info('logging out...')

        await ctx.bot.logout()

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: comms.Context) -> None:
        """Giving help to a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            The return value is always None.

        """
        lst = [
            '`Help is most likely not ready yet, check the link just in case:`',
            markdown_link('Help with commands link', 'https://github.com/Xithrius/Xythrion#commands')
        ]
        embed = discord.Embed(description='\n'.join(map(str, lst)))
        await ctx.send(embed=embed)


if __name__ == "__main__":
    if not os.path.isdir(path('tmp')):
        os.mkdir(path('tmp'))

    log = _rich_logger('info')

    bot = Xythrion(
        command_prefix=';', case_insensitive=True, help_command=None, log=log
    )

    try:
        bot.run(bot.config['discord'], bot=True, reconnect=True)

    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        log.info('Improper token has been passed.')

    _cleanup()
