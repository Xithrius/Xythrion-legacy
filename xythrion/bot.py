"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info

Running the bot:

    These instructions are also available in the "Setup" section of the README.

    NOTE: The following steps below assume that you have Python 3.8.x installed.
          It is assumed that "python3 -V" outputs Python 3.8.x if on Linux.
          If on Windows, replace "python3" with "py -3.8", "python", or "py".

    NOTE: ALTERNATIVES #1 AND #2 FOR THE VIRTUAL ENVIRONMENT SETUP AND THE SETUP WITHOUT
          ANY VIRTUAL ENVIRONMENT ASSUME THAT YOU'VE INSTALLED POSTGRESQL
          ON YOUR SYSTEM AND YOU'VE INSERTED YOUR CREDENTIALS INTO THE ".env" FILE.

    No virtual environment setup steps:
        Installing requirements:
            $ python3 -m pip install -r requirements.txt

        Running the bot:
            $ clear && python3 -m xythrion

    Creating the virtual environment and running the bot (3 ways):
        NOTE: DO NOT UPGRADE "pip" YOU'RE RUNNING THIS ON UBUNTU.

        Alternative #1 - virtualenv/venv:
            $ python3 -m pip install --U pip virtualenv
            $ python3 -m virtualenv venv
            $ source venv/Scripts/activate
            $ python3 -m xythrion

        Alternative #2 - pipenv:
            $ python3 -m pip install --U pip pipenv
            $ pipenv install --dev
            $ pipenv shell
            $ pipenv start run

        Alternative #3 - Docker:
            NOTE: IF YOU PLAN TO RUN THIS ALTERNATIVE ON WINDOWS 10,
                  YOU MUST HAVE WINDOWS 10 PRO.
            NOTE: IF YOU'RE ON LINUX MAKE SURE YOU HAVE CORRECTLY INSTALLED DOCKER BEFORE
                  RUNNING THESE COMMANDS.

            $ cp .env-example .env

            NOTE: Put as much information as you can into the .env file before running the final command in
                  this alternative.
            $ docker pull postgres

            NOTE: After running this command, be sure to replace "your_password_here" in the .env file,
                  with the password you have selected. This should be on the same line as "POSTGRES_PASSWORD"
            $ docker run --name postgres -e POSTGRES_PASSWORD=your_password_here -d postgres
            $ docker-compose up --build

"""


import asyncio
import os
from typing import Optional, Union, List
from datetime import datetime
from pathlib import Path

import aiohttp
import asyncpg
import discord
import humanize
from discord.ext import commands as comms
from discord.ext.commands import Bot, Cog, Context
from logging import getLogger

from .utils import markdown_link
from .constants import Postgresql


log = getLogger(__name__)


class Xythrion(Bot):
    """A subclass where very important tasks and connections are created.

    Attributes:
        loop (:obj:`asyncio.AbstractEventLoop`): The loop that executors will run off of.
        pool (:obj:`asyncpg.Pool`): Connection pool for database executions.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of tasks and connections.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)

        # Setting the loop.
        self.loop = asyncio.get_event_loop()

        # Checking and connecting to the postgresql database.
        try:
            self.loop.run_until_complete(self.check_and_connect_database())
            log.info('Asynchronous connection to Postgresql database has been setup.')

        except Exception as e:
            log.critical(f'Database failed setup. Parts of bot will not work.\nError: {e}')

        # Creating the session for getting information from URLs by fetching with GETs.
        self.session = aiohttp.ClientSession()

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Loading the rest of the extensions, one by one.
        # asyncio.get_event_loop().run_until_complete(self.load_extensions())

    async def check_and_connect_database(self) -> None:
        """Creates asynchronous database and session connection.

        Checks if the database has the correct tables before starting the bot up

        Returns:
            :obj:`type(None)`: Always None

        Raises:
           :obj:`asyncpg.PostgresSyntaxError`: Incorrect syntax in table creation.

        """
        self.pool = await asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60)

        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Links(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITH TIME ZONE NOT NULL,
                    id BIGINT,
                    name TEXT,
                    link TEXT
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS Snippets(
                    identification serial PRIMARY KEY,
                    t TIMESTAMP WITH TIME ZONE NOT NULL,
                    id BIGINT,
                    name TEXT,
                    code TEXT
                )
            ''')

    async def load_extensions(self, blocked_extensions: Optional[Union[str, list]] = None) -> None:
        """Loading in the extensions for the bot.

        Args:
            blocked_extensions (:obj:`typing.Union[str, list]`, optional): Extension(s) to not be loaded.

        Returns:
            :obj:`type(None)`: Always None

        Raises:
            :obj:`discord.ext.commands.ExtensionNotFound`: The extension could not be imported.
            :obj:`discord.ext.commands.NoEntryPointError`: The extension does not have a setup function.
            :obj:`discord.ext.commands.ExtensionFailed`:
                The extension or its setup function had an execution error.

        """
        broken_extensions = []

        for extension in await self.get_extensions():
            try:
                self.load_extension(extension)

            except Exception as e:
                broken_extensions.append((extension, e))

        for extension, error in broken_extensions:
            log.critical(f'{extension} could not be loaded: {error}')

    async def get_extensions(self) -> List[str]:
        """Acquiring extensions for the bot to load in.

        Returns:
            :obj:`typing.List[str]`: A list containing cogs.

        Raises:
            FileNotFoundError: When the folder 'cogs' cannot be found.

        """
        extensions = []

        for folder in os.listdir(Path(self.n, 'extensions')):
            extensions.extend(
                [f'{self.n}.extensions.{folder}.{i[:-3]}' for i in os.listdir(
                    Path(self.n, 'extensions', folder)) if i[-3:] == '.py']
            )

        return extensions

    async def on_ready(self) -> None:
        """Updates the bot status when logged in successfully.

        Returns:
            :obj:`type(None)`: Always None

        Raises:
           :obj:`discord.InvalidArgument`: If the activity type is invalid.

        """
        await self.wait_until_ready()

        self.startup_time = datetime.now()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="graphs")
        )

        log.info('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connections are closed properly.

        Returns:
            :obj:`type(None)`: Always None

        """
        try:
            await asyncio.wait(
                fs={self.session.close(), self.pool.close()},
                timeout=30.0, loop=self.loop, return_when=asyncio.ALL_COMPLETED
            )

        except asyncio.TimeoutError:
            log.critical('Waiting for final tasks to complete timed out after 30 seconds. Skipping.')

        log.info('finished up closing tasks.')

        return await super().logout()


class Development(Cog):
    """Cog required for development and control, along with the help command.

    Attributes:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    @comms.is_owner()
    async def _reload(self, ctx: Context, cog: Optional[str] = None) -> None:
        """Gets the cogs within folders and loads them into the bot after unloading current cogs.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Raises:
            Anything besides discord.ext.commands.ExtensionNotLoaded when loading cogs.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]r
            >>> [prefix]refresh

        """
        d = datetime.now()
        for cog in await self.bot.get_extensions():

            # Attempting to unload the load the extension back in.
            try:
                self.bot.reload_extension(cog)

            # If the extension was created after the bot initialized startup.
            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            # If a fatal error occurs.
            except Exception as e:
                await ctx.send(f'Error while reloading: {cog} - {e}')
                return log.warning(f'Reloading {cog} error: {e}')

        log.info((
            "Reloaded extensions in "
            f"{humanize.naturaldelta(d - datetime.now(), minimum_unit='milliseconds')}"
        ))

    @comms.command(name='logout', hidden=True)
    @comms.is_owner()
    async def _logout(self, ctx: Context) -> None:
        """Makes the bot Log out..

        NOTE: If in Docker, the current instance will die and another will be created.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: Always None

        """
        await self.bot.logout()

    @comms.command(name='loaded', hidden=True)
    @comms.is_owner()
    async def _loaded_extensions(self, ctx: Context) -> None:
        """Gives a list of the currently loaded cogs.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]loaded

        """
        lst = [f'{str(i).zfill(3)} | {k}' for i, k in enumerate(self.bot.cogs.keys())]
        c = '\n'.join(str(y) for y in lst)

        embed = discord.Embed(title='*Currently loaded cogs:*', description=f'```py\n{c}\n```')

        await ctx.send(embed=embed)

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: Context) -> None:
        """Giving help to a user.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: Always None

        Command example(s):
            >>> [prefix]help
            >>> [prefix]help graph

        """
        lst = [
            '`Help is most likely not ready yet, check the link just in case:`',
            markdown_link('Help with commands link', 'https://github.com/Xithrius/Xythrion#commands')
        ]

        embed = discord.Embed(description='\n'.join(map(str, lst)))

        await ctx.send(embed=embed)

    @comms.command(name='issue', aliases=['problem', 'issues'])
    async def _issue(self, ctx: Context) -> None:
        """Gives the user the place to report issues.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: Always None

        Command example(s):
            >>> [prefix]issue

        """
        url = 'https://github.com/Xithrius/Xythrion/issues'
        embed = discord.Embed(description=markdown_link('Report issue(s) here', url))

        await ctx.send(embed=embed)
