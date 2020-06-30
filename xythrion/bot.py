"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info

Running the bot:

    NOTE: The following steps below assume that you have Python 3.7.7 installed.

    Creating the virtual environment. (defaulting to "py", replace if needed):
        NOTE: DO NOT INCLUDE "pip" YOU'RE RUNNING THIS ON UBUNTU.
        $ py -3.7 -m pip install --upgrade pip virtualenv

        # Creating the virtual environment, then activating it.
        $ py -3.7 -m virtualenv venv
        $ source venv/Scripts/activate

    Installing requirements:
        $ py -3.7 -m pip install -r requirements.txt

    Running the bot:
        Windows:
            $ py -3.7 bot.py

        Linux/OSX:
            $ clear && python3 bot.py

"""


import asyncio
import datetime
import json
import os
from pathlib import Path
import typing as t

import asyncpg
import discord
from discord.ext import commands as comms

from .utils import markdown_link, tracebacker


class Xythrion(comms.Bot):
    """A subclass where very important tasks and connections are created.

    Attributes:
        config (dict): Tokens and other items from `./config/config.json`.
        loop (:obj:`asyncio.AbstractEventLoop`): The loop that executors will run off of.
        pool (:obj:`asyncpg.Pool`): Connection pool for database executions.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of tasks and connections.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            type(None): Always None.

        """
        # Name of folder the bot's operating in
        self.n = Path.cwd().name.lower()

        # Setting the logger before inheritence occurs.
        self.log, self.loop = kwargs.pop('log'), kwargs.pop('loop')

        # Initializing the base class `Comms.bot` and inheriting all it's attributes and functions.
        super().__init__(*args, **kwargs)

        # Attempting to open config config
        try:
            with open(Path.cwd() / 'config' / 'config.json') as f:
                self.config = json.load(f)

        # If the file could be found but not indexed properly.
        except IndexError as e:
            self.log.critical(f'{e}: Config file found, but token(s) could not be read properly.')

        # If the file could not be found.
        except FileNotFoundError as e:
            self.log.critical(f'{e}: Config file not found. Please refer to the README when setting up.')

        # Checking and connecting to the postgresql database.
        try:
            self.loop.run_until_complete(self.check_and_connect_database())

        except Exception as e:
            tracebacker(e)
            self.log.critical('Database failed setup. Killing bot initialization.')
            return

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Loading the cogs in, one by one.
        asyncio.get_event_loop().run_until_complete(self.load_extensions())

    async def check_and_connect_database(self) -> None:
        """Creates asynchronous database and session connection.

        Checks if the database has the correct tables before starting the bot up

        Returns:
            bool: True if the database failed to check and/or connect,
                None if there are no errors.

        Raises:
           :obj:`asyncpg.PostgresSyntaxError`: Incorrect syntax in table creation.

        """
        self.pool = await asyncpg.create_pool(**self.config['db'], command_timeout=60)

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

    async def load_extensions(self, blocked_extensions: t.Optional[t.Union[str, list]] = None) -> None:
        """Loading in the extensions for the bot.

        Args:
            blocked_extensions (:obj:`t.Union[str, list]`, optional): Extension(s) to not be loaded.

        Returns:
            type(None): Always None.

        Raises:
            :obj:`ExtensionNotFound`: The extension could not be imported.
            :obj:`NoEntryPointError`: The extension does not have a setup function.
            :obj:`ExtensionFailed`: The extension or its setup function had an execution error.

        """
        extensions = await self.get_extensions()
        broken_extensions = []

        for extension in extensions:
            try:
                self.load_extension(extension)

            except Exception as e:
                broken_extensions.append((extension, e))

        for extension, error in broken_extensions:
            self.log.critical(f'{extension} could not be loaded: {error}')

    async def get_extensions(self) -> t.List[str]:
        """Acquiring extensions for the bot to load in.

        Returns:
            :obj:`t.List[str]`: A list containing cogs.

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
            type(None): Always None.

        Raises:
           :obj:`discord.InvalidArgument`: If the activity type is invalid.

        """
        await self.wait_until_ready()

        self.startup_time = datetime.datetime.now()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="graphs")
        )

        self.log.warning('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connections are closed properly.

        Returns:
            type(None): Always None.

        Raises:
            TODO: What happens when self.pool.close() fails?

        """
        self.log.info('Closing database connection pool.')

        await self.pool.close()

        return await super().logout()


class Development(comms.Cog):
    """Cog required for development and control, along with the help command.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        Returns:
            type(None): Always None.

        """
        self.bot = bot

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    @comms.is_owner()
    async def _reload(self, ctx: comms.Context) -> None:
        """Gets the cogs within folders and loads them into the bot after unloading current cogs.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Raises:
            Anything besides comms.ExtensionNotLoaded when loading cogs.

        Command examples:
            >>> [prefix]r
            >>> [prefix]refresh

        """
        for cog in await self.bot.get_extensions():

            # Attempting to unload the load the extension back in.
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            # If the extension was created after the bot initialized startup.
            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            # If a fatal error occurs.
            except Exception as e:
                return self.bot.log.warning(f'Error while loading "{cog}" error: {e}')

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='restart', hidden=True)
    @comms.is_owner()
    async def _restart(self, ctx: comms.Context) -> None:
        pass

    @comms.command(name='loaded', hidden=True)
    @comms.is_owner()
    async def _loaded_extensions(self, ctx: comms.Context) -> None:
        """Gives a list of the currently loaded cogs.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            type(None): Always None.

        Command examples:
            >>> [prefix]loaded

        """
        lst = [f'{str(i).zfill(3)} | {k}' for i, k in enumerate(self.bot.cogs.keys())]
        c = '\n'.join(str(y) for y in lst)

        embed = discord.Embed(title='*Currently loaded cogs:*', description=f'```py\n{c}\n```')

        await ctx.send(embed=embed)

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    @comms.is_owner()
    async def _exit(self, ctx: comms.Context) -> None:
        """Makes the bot logout.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            type(None): Always None.

        Command examples:
            >>> [prefix]exit

        """
        self.bot.log.warning('logging out...')

        await ctx.bot.logout()

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: comms.Context) -> None:
        """Giving help to a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            type(None): Always None.

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
    async def _issue(self, ctx: comms.Context) -> None:
        """Gives the user the place to report issues.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            type(None): Always None.

        Command example(s):
            >>> [prefix]issue

        """
        url = 'https://github.com/Xithrius/Xythrion/issues'
        embed = discord.Embed(description=markdown_link('Report issue(s) here', url))

        await ctx.send(embed=embed)
