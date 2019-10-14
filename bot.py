"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Running the bot:
    First time usage:
        $ py -3 -m pip install --user -r requirements.txt
    Starting the bot:
        $ py -3 bot.py

Todo:
    * Redo items here to make everything clean and simple
    * Make bot available for everyone (exception is reload and exit commands)
    * Request pool
"""


import click
import logging
import json
import collections
import os
import asyncio
import datetime
import sys
import traceback
import asyncpg
import aiohttp

from discord.ext import commands as comms
import discord

from modules.output import path, cs, get_extensions


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=path('tmp', 'discord.log'), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Xythrion(comms.Bot):
    """Creating connections, attributes, and background tasks.

    Preface: When ctx is args, it gives context on where the method was called, such as channel, member, and guild.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #: Opening the config json file
        with open(path('config', 'config.json'), 'r', encoding='utf8') as f:
            data = json.load(f)

        #: Giving self.config recursive attributes from config.json
        self.config = json.loads(json.dumps(data), object_hook=lambda d: collections.namedtuple('config', d.keys())(*d.values()))

        self.ec = 0xe67e22

        #: Create async loop
        self.loop = asyncio.get_event_loop()

        future = asyncio.gather()
        self.loop.create_task(self.create_tasks())
        self.loop.run_until_complete(future)


    """ subclass-specific functions """

    async def create_tasks(self):
        """Session and database connections while testing service status.

        Raises:
            Errors depending on connection success/fail

        """
        await self.check_database()

        self.s = aiohttp.ClientSession()
        cs.r('Session established successfully.')

        self.db_connection = asyncio.get_running_loop()
        await self.db_connection.create_task(self.check_database())

    async def check_database(self):
        with open(path('config', 'config.json'), 'r') as f:
            data = json.load(f)['db']
            self.conn = await asyncpg.connect(**data)

        await self.conn.execute('''CREATE TABLE IF NOT EXISTS Runtime(id serial PRIMARY KEY, login TIMESTAMP, logout TIMESTAMP)''')
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS Messages(id serial PRIMARY KEY, identification BIGINT, messages INTEGER, images INTEGER, videos INTEGER, audios INTEGER)''')
        # await self.conn.execute('''CREATE TABLE IF NOT EXISTS Users(id serial PRIMARY KEY, identification BIGINT)''')

    """ Events """

    async def on_ready(self):
        """Bot event is activated once login is successful.
        
        Returns:
            Success or failure message(s)

        Raises:
            An exception as e if something went wrong while loading extensions.

        """
        self.login_time = datetime.datetime.now()
        cs.w('Loading extensions...')
        broken_extensions = []
        for extension in get_extensions():
            try:
                self.load_extension(extension)
            except Exception as e:
                broken_extensions.append(f'{extension} - {e}')
        for ext in broken_extensions:
            cs.w(ext)
        await self.change_presence(status=discord.ActivityType.playing, activity=discord.Game('with user data'))
        cs.r('Startup completed.')

    async def close(self):
        """ Safely closes connections

        Returns & Raises:
            Nothing since they're all passed.
        
        """
        try:
            await self.s.close()
            await self.conn.close()
        except Exception:
            pass
        await super().close()


class MainCog(comms.Cog, command_attrs=dict(hidden=True, case_insensitive=True)):
    """Essential commands for using the bot."""

    def __init__(self, bot):

        #: Setting Xythrion(comms.Bot) as a class attribute
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        """Checks if the command caller is an owner.

        Returns:
            True or false, depending on the contents of config.json's owner data.

        """
        return await self.bot.is_owner(ctx.author)

    @comms.command(aliases=['refresh', 'r'])
    async def reload(self, ctx):
        """Finds all cogs within the 'cogs' directory then loads/unloads them.

        Returns:
            Success or faliure message depending on extension loading

        """
        broken_extensions = []
        for ext in get_extensions():
            try:
                self.bot.unload_extension(ext)
                self.bot.load_extension(ext)
            except discord.ext.commands.ExtensionNotLoaded:
                self.bot.load_extension(ext)
            except Exception as e:
                broken_extensions.append(f'{ext} - {e}')
        if broken_extensions:
            info = '\n'.join(y for y in broken_extensions)
            await ctx.send(f'```\n{info}```', delete_after=15)
        else:
            await ctx.send('Reloaded all extensions.', delete_after=5)

    @comms.command(aliases=['disconnect', 'dc'])
    async def exit(self, ctx):
        """Logs out the bot.

        Returns:
            A possible timeout error.

        """
        await self.bot.conn.execute('''INSERT INTO Runtime(login, logout) VALUES($1, $2)''', self.bot.login_time, datetime.datetime.now())
        cs.w('Logging out...')
        await ctx.bot.logout()

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Catches errors caused by users

        Returns:
            An error message only if the error is caused by a user, and not the bot.

        Raises:
            A traceback message if there's an internal error

        """
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, comms.DisabledCommand):
            return await ctx.send(cs.css(f'Command {ctx.command} not available.'))

        elif isinstance(error, comms.CommandNotFound):
            return await ctx.send(cs.css(f'Command {ctx.command} not found.'))

        elif isinstance(error, comms.UserInputError):
            return await ctx.send(cs.css(f'Command {ctx.command} raised bad argument: {error}'))
        
        elif isinstance(error, comms.NotOwner):
            return await ctx.send(cs.css('You do not own enough permissions to do this command.'))

        else:
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


if __name__ == "__main__":
    bot = Xythrion(command_prefix=comms.when_mentioned_or(';'))
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
