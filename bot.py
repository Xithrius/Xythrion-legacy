'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import datetime
import traceback
import configparser
import os

import discord
from discord.ext import commands as comms

import relay
from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Main cog
# //////////////////////////////////////////////////////////////////////////// #
# Items that are included are essential to running the bot
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    def __init__(self, bot, cogs):
        """ Objects: Bot, list of cogs to be loaded, background task(s) """
        self.bot = bot
        self.cogs = cogs
        self.load_cog_task = self.bot.loop.create_task(self.load_cogs_in())

# //////////////////////////////////////////////// # Background tasks

    async def load_cogs_in(self):
        """ Load the cogs in after the bot is ready """
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

    @comms.Cog.listener()
    async def on_ready(self):
        """ Event activates when bot is ready for use """
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        await self.bot.change_presence(activity=discord.Game(f'with pixels'))
        start = f"""

         [{now}]
    +----[ Relay.py ]------------------------------------------------------+
    |    Copyright (c) 2019 Xithrius
    |    MIT license, Refer to LICENSE for more info
    +----------------------------------------------------------------------+
    |    ID      --->   {self.bot.user.id}
    |    Booting --->   {self.bot.user}
    +----------------------------------------------------------------------+
    |    Using discord.py {discord.__version__}
    |    Using relay.py {relay.__version__}
    |    Changed status to 'Playing with pixels'
    |    Awaiting...
    +----------------------------------------------------------------------+

        """
        print(start)

# //////////////////////////////////////////////// # Commands

    @comms.command(name='r', hidden=True)
    @comms.is_owner()
    async def reload_cogs(self, ctx):
        """ Reload all cog """
        loaded_cogs = []
        broken_cogs = []
        for cog in self.cogs:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                broken_cogs.append(f'{cog}: {type(e).__name__} - {e}\n')
            else:
                loaded_cogs.append(cog)
        if len(broken_cogs) > 0:
            print(f"Cog(s) could not be reloaded:\n{', '.join(str(y) for y in broken_cogs)}")
        if len(loaded_cogs) > 0:
            print(f"Cog(s) reloaded:\n{', '.join(str(y) for y in loaded_cogs)}")
        else:
            print(f"No cogs were reloaded.")

    @comms.command(name='l', hidden=True)
    @comms.is_owner()
    async def load_cog(self, ctx, cog):
        """ Load a specific cog """
        if cog in self.cogs:
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                print(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            print(f'Cog {cog} is blocked or does not exist.')

    @comms.command(name='u', hidden=True)
    @comms.is_owner()
    async def unload_cog(self, ctx, cog):
        """ Unload a specific cog """
        if cog in self.cogs:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                print(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            print(f'Cog {cog} is blocked or does not exist.')

    @comms.command(name='exit', hidden=True)
    @comms.is_owner()
    async def logout(self, ctx):
        """ Make the bot logout """
        await self.bot.logout()

    @comms.command(name='reload', hidden=True)
    @comms.is_owner()
    async def reload(self, ctx):
        """ Reload the entire bot """
        await ctx.send('Nothing here yet')


# //////////////////////////////////////////////////////////////////////////// #
# Setup bot function                                                           #
# //////////////////////////////////////////////////////////////////////////// #
# Used for passing objects into the main cog to run the bot                    #
# //////////////////////////////////////////////////////////////////////////// #


def setup_bot(bot=comms.Bot(command_prefix='$')):
    """ Passing objects into the MainCog, then running the bot """
    # Searching for cogs within the cogs directory
    essential_cogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
        essential_cogs.extend(filenames)
        break
    custom_cogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs', 'rack')):
        custom_cogs.extend(filenames)
        break
    # Creating the list of extensions
    cogs = []
    for file in essential_cogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.{file[:-3]}')
    for file in custom_cogs:
        if file[-3:] == '.py':
            cogs.append(f'cogs.rack.{file[:-3]}')
    # Blocking cogs, if any at all
    for i in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r')]:
        for j in cogs:
            if j in [f'cogs.{i}', f'cogs.rack.{i}']:
                cogs.pop(cogs.index(j))
    bot.add_cog(MainCog(bot, cogs))
    bot.remove_command('help')
    # Looping the input until token is correct
    checkToken = True
    while checkToken:
        try:
            config = configparser.ConfigParser()
            config.read(path('relay', 'configuration', 'config.ini'))
            token = config['discord']['token']
            bot.run(token, bot=True, reconnect=True)
            checkToken = False
        except FileNotFoundError or discord.errors.LoginFailure:
            token = input('Input discord bot token: ')
            config = configparser.ConfigParser()
            config['discord'] = {'token': token}
            with open(path('relay', 'configuration', 'config.ini'), 'w') as f:
                config.write(f)


if __name__ == '__main__':
    setup_bot()
else:
    print('Bot cannot be booted from another location.')
