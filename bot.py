'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import os
import sys
import traceback
import aiohttp
import datetime
import configparser

import discord
from discord.ext import commands as comms

from essentials.pathing import path  # , mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# //////////////////////////////////////////////////////////////////////////// #
# The Main Cog
# /////////////////////////////////////////////////////////
# Where all extensions automatically detected and loaded into
# Only the essential commands and event are here
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='r', hidden=True)
    @comms.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """ Reload specific cog(s) """
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Reload complete for {cog}')

# ////////////////////////

    @comms.command(name='load', hidden=True)
    @comms.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """ Load in a specific cog(s) """
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Load complete for {cog}')

    @comms.command(name='unload', hidden=True)
    @comms.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """ Unload a specific cog(s) """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Reload error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Unload complete for {cog}')

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

# Events
    @comms.Cog.listener()
    async def on_ready(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        await bot.change_presence(activity=discord.Game(f'discord.py rewrite {discord.__version__}'))
        print()
        print(f"+---[{now}]---------------------------------------+")
        print("|                                                                      |")
        print("|    ______                           _           _ _                  |")
        print("|    |  _  \\                         (_)         | | |                 |")
        print("|    | | | |___ _ __ ___   ___  _ __  _  ___ __ _| | |_   _            |")
        print("|    | | | / _ \\ '_ ` _ \\ / _ \\| '_ \\| |/ __/ _` | | | | | |           |")
        print("|    | |/ /  __/ | | | | | (_) | | | | | (_| (_| | | | |_| |           |")
        print("|    |___/ \\___|_| |_| |_|\\___/|_| |_|_|\\___\\__,_|_|_|\\__, |           |")
        print("|                                                      __/ |           |")
        print("|                                                      |___/           |")
        print("|                                                                      |")
        print(f"|    Booting --->   {self.bot.user}                                   |")
        print(f"|    ID      --->   {self.bot.user.id}                                 |")
        print("|                                                                      |")
        print("|    Awaiting...                                                       |")
        print("|                                                                      |")
        print("+----------------------------------------------------------------------+")
        print()
        print(f"Presence changed to 'discord.py {discord.__version__}'")


# ///////////////////////////////////////////////////////// #
# Starting the bot
# ////////////////////////
# All extensions automatically detected and loaded
# A config file is used for the bot token
# ///////////////////////////////////////////////////////// #


def main(bot=False):
    if not bot:
        bot = comms.Bot(connector=aiohttp.TCPConnector(ssl=False), command_prefix='$')
        print('Booting with setup...')

    # Adding the main cog to the bot
    bot.add_cog(MainCog(bot))
    bot.remove_command('help')

    # Searching for cogs within the cogs directory
    fileCogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
        fileCogs.extend(filenames)
        break

    # Making the names of cogs start with cogs.
    cogs = []
    for file in fileCogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.{file[:-3]}')

    # Removing cogs if they're in the unload list
    finalCogs = []
    with open(path('configuration', 'cog_unload.txt'), 'r') as f:
        for i in cogs:
            for x in f:
                if i != f'cogs.{x}':
                    finalCogs.append(i)

    # Loading all cogs in as extensions of the main cog
    for i in finalCogs:
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
