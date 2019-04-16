'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import os
import sys
import traceback
import aiohttp
import datetime
import configparser

import discord
from discord.ext import commands as comms

from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Main cog
# /////////////////////////////////////////////////////////
# Items that are essential to running the bot properly
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// #
    @comms.command(name='r_b', hidden=True)
    async def reload_background_task(self, ctx):
        pass

    # //////////////////////// #
    @comms.command(name='ra_b', hidden=True)
    async def reload_all_background_tasks(self, ctx):
        pass

    # //////////////////////// # Reloading a singular cog
    @comms.command(name='r_c', hidden=True)
    @comms.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """ Reload specific cog(s) """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Reload complete for {cog}')

    # //////////////////////// # Reloading all cogs that exist
    @comms.command(name='ra_c', hidden=True)
    @comms.is_owner()
    async def reload_all_custom_cogs(self, ctx, option=None):
        cogs = []
        with open(path('configuration', 'listed_cogs.txt'), 'r') as f:
            for x in f:
                
            cogs.append()

        for cog in cogs:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'Reload error: {type(e).__name__} - {e}')
            else:
                await ctx.send(f'Reload complete for {cog}')

    # //////////////////////// # Loading cog(s)
    @comms.command(name='load', hidden=True)
    @comms.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """ Load in a specific cog(s) """
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Load complete for {cog}')

    # //////////////////////// # Unloading cog(s)
    @comms.command(name='unload', hidden=True)
    @comms.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """ Unload a specific cog(s) """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Unload complete for {cog}')

    # //////////////////////// # Making the bot log out, and remove all big files
    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        """ Make the bot logout, while cleaning up files """
        music = []
        for (dirpath, dirnames, filenames) in os.walk(path('audio', 'music')):
            music.extend(filenames)
            break
        try:
            for i in music:
                os.remove(path('audio', 'music', i))
            os.remove(path('audio', 'output.mp3'))
        except FileNotFoundError:
            pass
        print('Exiting...')
        await self.bot.logout()

# //////////////////////////////////////////////// # Events
    # //////////////////////// # When the bot is ready, this message will be printed
    @comms.Cog.listener()
    async def on_ready(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        await bot.change_presence(activity=discord.Game(f'discord.py rewrite {discord.__version__}'))
        start = f"""

    +----[ Demonically ]---------------------------------------------------+
    |
    |    Copyright (c) 2019 Xithrius
    |    MIT license, Refer to LICENSE for more info
    |
    +----[{now}]--------------------------------------+
    |
    |    ID      --->   {self.bot.user.id}
    |    Booting --->   {self.bot.user}
    |
    +----------------------------------------------------------------------+
    |
    |    playing discord.py {discord.__version__}...
    |    Awaiting...
    |
    +----------------------------------------------------------------------+

        """
        print(start)


# //////////////////////////////////////////////////////////////////////////// #
# Main
# /////////////////////////////////////////////////////////
# Sets up the bot with auto-detection of cogs that will be used, and configuration
# //////////////////////////////////////////////////////////////////////////// #


def main(bot=False):
    if not bot:
        bot = comms.Bot(connector=aiohttp.TCPConnector(ssl=False), command_prefix='$')
        print('Booting with setup...')

    # Adding the main cog to the bot
    bot.add_cog(MainCog(bot))
    bot.remove_command('help')

    # Searching for cogs within the cogs directory
    essential_cogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
        essential_cogs.extend(filenames)
        break

    custom_cogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs', 'seperate')):
        custom_cogs.extend(filenames)
        break

    # Creating the list of extensions
    cogs = []
    for file in essential_cogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.{file[:-3]}')
    for file in custom_cogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.seperate.{file[:-3]}')

    # Making a list of all blocked cogs
    blocked_cogs = []
    with open(path('configuration', 'blocked_cogs.txt'), 'r') as f:
        for x in f:
            blocked_cogs.append(f'cogs.{x}')

    with open(path('configuration', 'listed_cogs.txt'), 'a') as f:
        for i in cogs:
            if i not in blocked_cogs:
                f.write(i)

    # Loading all cogs in as extensions of the main cog
    for i in cogs:
        if i not in blocked_cogs:
            try:
                bot.load_extension(i)
            except Exception as e:
                print(e)
                print(f'Failed to load extension {i}.', file=sys.stderr)
                traceback.print_exc()

    # Looping the input until token is correct
    checkToken = True
    while checkToken:
        try:
            config = configparser.ConfigParser()
            config.read(path('configuration', 'config.ini'))
            token = config['discord']['token']
            bot.run(token, bot=True, reconnect=True)
            checkToken = False
        except FileNotFoundError or discord.errors.LoginFailure:
            token = input('Input discord bot token: ')
            config = configparser.ConfigParser()
            config['discord'] = {'token': token}
            with open(path('configuration', 'config.ini'), 'w') as f:
                config.write(f)


if __name__ == '__main__':
    bot = comms.Bot(connector=aiohttp.TCPConnector(ssl=False), command_prefix='$')
    print('Booting without setup...')
    main(bot)
