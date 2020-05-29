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
import concurrent.futures
import datetime
import json
import logging
import os
import typing as t

import asyncpg
import discord
from discord.ext import commands as comms
from rich import logging as r_logging, r_traceback

from utils import markdown_link, path, tracebacker


def _discord_logger(log_type: t.Union[str, int] = None) -> None:
    """Logs information specifically for discord.

    Args:
        log_type (:obj:`t.Union[str, int]`, optional): The level of logging to be used.
            Defaults to None.

    Returns:
        bool: Always None.

    """
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    if not os.path.isdir(path(f'tmp{os.sep}')):
        os.mkdir(path('tmp'))

    base_handler = logging.FileHandler(filename=path('tmp', 'discord.log'), encoding='utf-8', mode='w')
    base_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(base_handler)


def _rich_logger(log_type: t.Union[str, int] = None, store_logs: bool = False) -> logging.Logger:
    """Logs information with the rich library with fancy tracebacks.

    Args:
        log_type (:obj:`t.Union[str, int]`, optional): The level of logging to be used.
            Defaults to None.
        store_file (bool, optional): If the logs want to be stored.

    Returns:
        :obj:`logging.Logger`: The object that the bot will use to log information to.

    Raises:
        IndexError: If `log_type` isn't within log_types.

    """
    r_traceback.install()

    log_types = {'info': logging.INFO, 'debug': logging.DEBUG, None: 'NOTSET'}

    logger = logging.getLogger('rich')

    if store_logs:
        _discord_logger(log_types[log_type])

    else:
        handler = r_logging.RichHandler()
        handler.setFormatter(logging.Formatter('%(messages)', datefmt='[%c]'))

    handler.setLevel(log_types[log_type])

    return logger


def _cleanup(folders: t.Union[list, str] = 'tmp') -> None:
    """Cleans up folders after the running of the bot's blocking stops.

    Function will continue clearing files until it is done or a folder cannot be found.

    NOTE: THIS FUNCTION WILL DESTROY ALL FILES CONTAINING '.log', '.pycache', AND/OR '.png'.
          USE THIS FUNCTION WITH CARE.

    Args:
        folders (:obj:`t.Union[list, str]`, optional): Folder to have their contents cleared out.

    Returns:
        bool: Always None.

    Raises:
        FileNotFoundError: If one of the specified folders cannot be found.

    """
    folders = [folders] if isinstance(folders, str) else folders

    for folder in folders:
        if os.path.isdir(path(folder)):
            for item in os.listdir(path(folder)):
                if ['.log', '.pycache', '.png'] in item[-4:]:
                    os.remove(path(folder, item))

        else:
            raise FileNotFoundError(f'Folder {folder} could not be located.')


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
            bool: Always None.

        """
        # Setting the logger before inheritence occurs.
        self.log = kwargs.pop('log')

        # Initializing the base class `Comms.bot` and inheriting all it's attributes and functions.
        super().__init__(*args, **kwargs)

        # Attempting to open config config
        try:
            with open(path('config', 'config.json')) as f:
                self.config = json.load(f)

        # If the file could be found but not indexed properly.
        except IndexError as e:
            self.log.info(f'{e}: Config file found, but token(s) could not be read properly.')

        # If the file could not be found.
        except FileNotFoundError as e:
            self.log.info(f'{e}: Config file not found. Please refer to the README when setting up.')

        # Create asyncio loop
        self.loop = asyncio.get_event_loop()

        # Create executor for running sync functions asynchronously
        self.executor = concurrent.futures.ThreadPoolExecutor()

        # Checking and connecting to the postgresql database.
        fail = self.loop.run_until_complete(self.check_and_connect_database())

        # If the database failed in some way.
        if fail:
            return

        # Add the main cog required for development and control.
        self.add_cog(Development(self))

        # Loading the cogs in, one by one.
        asyncio.get_event_loop().run_until_complete(self.load_extensions())

    async def check_and_connect_database(self) -> t.Union[True, None]:
        """Creates asynchronous database and session connection.

        Checks if the database has the correct tables before starting the bot up

        Returns:
            bool: True if the database failed to check and/or connect,
                None if there are no errors.

        Raises:
           :obj:`asyncpg.PostgresSyntaxError`: Incorrect syntax in table creation.

        """
        try:
            self.pool = await asyncpg.create_pool(**self.config['db'], command_timeout=60)

        except Exception as e:
            self.log.info(f'Fatal error while creating connection to database: {e}')
            return True

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

    async def load_extensions(self, blocked_extensions: t.Union[str, list] = None) -> None:
        """Loading in the extensions for the bot.

        Args:
            blocked_extensions (:obj:`t.Union[str, list]`, optional): Extension(s) to not be loaded.

        Returns:
            bool: Always None.

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
            tracebacker(error)

    async def get_extensions(self) -> t.List[str]:
        """Acquiring extensions for the bot to load in.

        Returns:
            :obj:`t.List[str]`: A list containing cogs.

        Raises:
            FileNotFoundError: When the folder 'cogs' cannot be found.

        """
        extensions = []

        for folder in os.listdir(path('cogs')):
            extensions.extend(
                [f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py']
            )

        return extensions

    async def on_ready(self) -> None:
        """Updates the bot status when logged in successfully.

        Returns:
            bool: Always None.

        Raises:
           :obj:`discord.InvalidArgument`: If the activity type is invalid.

        """
        await self.wait_until_ready()

        self.startup_time = datetime.datetime.now()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="graphs")
        )

        self.log.info('Awaiting...')

    async def logout(self) -> None:
        """Subclassing the logout command to ensure connections are closed properly.

        Returns:
            bool: Always None.

        Raises:
            TODO: What happens when self.pool.close() fails?

        """
        await self.pool.close()

        return await super().logout()


class Development(comms.Cog, description='development and help commands.'):
    """Cog required for development and control, along with the help command.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        Returns:
            bool: Always None.

        """
        self.bot = bot

    async def cog_check(self, ctx: comms.Context) -> t.Union[True, False]:
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
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
        for cog in await self.get_extensions():
            # Attempting to unload the load the extension back in.
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            # If the extension was created after the bot initialized startup.
            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)

            # If a fatal error occurs.
            except Exception as e:
                return self.log.info(f'Error while loading "{cog}" error: {e}')

        await ctx.send('Reloaded extensions.', delete_after=7)

    @comms.command(name='loaded', hidden=True)
    async def _loaded_extensions(self, ctx: comms.Context) -> None:
        """Gives a list of the currently loaded cogs.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]loaded

        """
        lst = [f'{str(i).zfill(3)} | {k}' for i, k in enumerate(self.bot.cogs.keys())]
        c = '\n'.join(str(y) for y in lst)

        embed = discord.Embed(title='*Currently loaded cogs:*', description=f'```py\n{c}\n```')

        await ctx.send(embed=embed)

    @comms.command(name='exit', aliases=['logout', 'disconnect'], hidden=True)
    async def _exit(self, ctx: comms.Context) -> None:
        """Makes the bot logout.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]exit

        """
        self.bot.log.info('logging out...')

        await ctx.bot.logout()

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: comms.Context) -> None:
        """Giving help to a user.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None

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


if __name__ == "__main__":
    # Creating the `tmp` directory if it doesn't exist
    if not os.path.isdir(path('tmp')):
        os.mkdir(path('tmp'))

    # Initializing the subclass of `comms.Bot`.
    bot = Xythrion(
        command_prefix=';', case_insensitive=True, help_command=None, log=_rich_logger('info')
    )

    # Attempting to run the bot (blocking, obviously).
    try:
        bot.run(bot.config['discord'], bot=True, reconnect=True)

    # If the token is incorrect or not given.
    except (discord.errors.HTTPException, discord.errors.LoginFailure):
        bot.log.info('Improper token has been passed.')

    # Removing any stray files within the `tmp` directory
    _cleanup()
