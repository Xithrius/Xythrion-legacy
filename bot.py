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
import datetime
import configparser
import traceback

import discord
from discord.ext import commands as comms

from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Main cog
# /////////////////////////////////////////////////////////
# Items that are included are essential to running the bot
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    # //////////////////////// # Object(s): 
    # bot, list of cogs to be loaded, background task(s)
    def __init__(self, bot, cogs):
        self.bot = bot
        self.cogs = cogs
        self.load_cog_task = self.bot.loop.create_task(self.load_cogs_in())

    def cog_unload(self):
        # self.bg_task.cancel()
        pass

# //////////////////////////////////////////////// # Background tasks
    # //////////////////////// # Load the cogs in after the bot is ready
    async def load_cogs_in(self):
        print("---> Booting cogs...")
        loaded_cogs = []
        broken_cogs = []
        await self.bot.wait_until_ready()
        if not self.bot.is_closed():
            for cog in self.cogs:
                try:
                    self.bot.load_extension(cog)
                except Exception as e:
                    broken_cogs.append(f'{cog}: {type(e).__name__} - {e}')
                    traceback.print_exc()
                else:
                    loaded_cogs.append(cog)
            if len(broken_cogs) > 0:
                print(f"Cog(s) could not be loaded:\n{', '.join(str(y) for y in broken_cogs)}")
            if len(loaded_cogs) > 0:
                print(f"Cog(s) loaded:\n{', '.join(str(y) for y in loaded_cogs)}")
            else:
                print(f"No cogs were loaded")

# //////////////////////////////////////////////// # Events
    # //////////////////////// # When the bot is ready, this message will be printed
    @comms.Cog.listener()
    async def on_ready(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        await self.bot.change_presence(activity=discord.Game(f'discord.py rewrite {discord.__version__}'))
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

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Reload a background task
    @comms.command(name='r_b', hidden=True)
    @comms.is_owner()
    async def reload_background_task(self, ctx):
        pass

    # //////////////////////// # Reload all background tasks
    @comms.command(name='ra_b', hidden=True)
    @comms.is_owner()
    async def reload_all_background_tasks(self, ctx):
        pass

    # //////////////////////// # Reload a cog
    @comms.command(name='r_c', hidden=True)
    @comms.is_owner()
    async def reload_cog(self, ctx, cog):
        loaded_cogs = []
        broken_cogs = []
        for cog in self.cogs:
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                broken_cogs.append(f'{cog}: {type(e).__name__} - {e}')
            else:
                loaded_cogs.append(cog)
        if len(broken_cogs) > 0:
            print(f"Cog(s) could not be loaded:\n{', '.join(str(y) for y in broken_cogs)}")
        if len(loaded_cogs) > 0:
            print(f"Cog(s) loaded:\n{', '.join(str(y) for y in loaded_cogs)}")
        else:
            print(f"No cogs were loaded")

    # //////////////////////// # Reload all cogs
    @comms.command(name='ra_c', hidden=True)
    @comms.is_owner()
    async def reload_all_cogs(self, ctx):
        for cog in self.cogs:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                print(f'Reload error: {type(e).__name__} - {e}')
            else:
                print(f'Reload complete for {cog}')

    # //////////////////////// # Logout the bot
    @comms.command(name='exit', hidden=True)
    @comms.is_owner()
    async def logout(self, ctx):
        await self.bot.logout()

    # //////////////////////// # Reload the bot itself
    @comms.command(name='r', hidden=True)
    @comms.is_owner()
    async def reload(self, ctx):
        pass # I'll do this at some point

# //////////////////////////////////////////////// # Passing objects into the MainCog
def main(bot=comms.Bot(connector=aiohttp.TCPConnector(ssl=False), command_prefix='$')):
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

    # Blocking cogs, if any at all
    blocked_cogs = []
    unblocked_cogs = []
    with open(path('configuration', 'blocked_cogs.txt'), 'r') as f:
        for x in f:
            for i in cogs:
                if i != f'cogs.{x[:-1]}' or f'cogs.seperate.{x[:-1]}':
                   unblocked_cogs.append(i)
    
    bot.add_cog(MainCog(bot, unblocked_cogs))
    bot.remove_command('help')

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
    main()
else:
    print('Booting from another location...')
