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


import traceback
import json
import os

import discord
from discord.ext import commands as comms

from containers.QOL.pathing import path
from containers.output.printer import duplicate, printc
import relay


# //////////////////////////////////////////////////////////////////////////// #
# Main cog
# //////////////////////////////////////////////////////////////////////////// #
# Items that are included are essential to running the bot
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    def __init__(self, bot, cogs):
        """ Objects:
        Bot
        List of cogs to be loaded
        Permernant list of cogs
        Background task
        """
        self.bot = bot
        self.cogs = cogs
        self.all_cogs = self.cogs
        self.presence = 'with pixels'
        self.load_cog_task = self.bot.loop.create_task(self.load_cogs_in())

    """

    Background tasks

    """
    async def load_cogs_in(self):
        """
        Load the cogs in after the bot is ready
        """
        printc('[...]: LOADING COGS')
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
                printc(f"WARNING: COG(S) COULD NOT BE LOADED:\n\t{', '.join(str(y) for y in broken_cogs)}")
            if len(loaded_cogs) > 0:
                printc(f"[ ! ]: COG(S) LOADED:\n\t{', '.join(str(y) for y in loaded_cogs)}")
            else:
                printc("WARNING: NO COG(S) HAVE BEEN LOADED")

    """

    Events

    """
    @comms.Cog.listener()
    async def on_ready(self):
        """
        Event activates when bot is ready for use
        """
        await self.bot.change_presence(activity=discord.Game(self.presence))
        start = f"""
    +----[ Relay.py ]------------------------------------------------------+
    |    Copyright (c) 2019 Xithrius
    |    MIT license, Refer to LICENSE for more info
    +----------------------------------------------------------------------+
    |    ID      --->   {self.bot.user.id}
    |    Booting --->   {self.bot.user}
    +----------------------------------------------------------------------+
    |    Using discord.py {discord.__version__}
    |    Using relay.py {relay.__version__}
    |    Changed status to 'Playing {self.presence}'
    |    Awaiting...
    +----------------------------------------------------------------------+
        """
        printc(start)

    """

    Commands

    """
    @comms.command(name='r', hidden=True)
    @comms.is_owner()
    async def reload_cogs(self, ctx):
        """
        Reload all cog
        """
        printc('[...]: RELOADING COGS')
        loaded_cogs = []
        broken_cogs = []
        for cog in self.cogs:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except comms.ExtensionNotLoaded:
                self.bot.load_extension(cog)
            except Exception as e:
                broken_cogs.append(f'{cog}: {type(e).__name__} - {e}\n')
            else:
                loaded_cogs.append(cog)
        if len(broken_cogs) > 0:
            await ctx.send(duplicate(f"WARNING: COG(S) COULD NOT BE RELOADED:\n\t{', '.join(str(y) for y in broken_cogs)}"), delete_after=10)
        if len(loaded_cogs) > 0:
            printc(f"[ ! ]: COG(S) RELOADED:\n\t{', '.join(str(y) for y in loaded_cogs)}")
            await ctx.send('Cogs have been reloaded successfully', delete_after=10)
        else:
            printc(f"WARNING: NO COG(S) HAVE BEEN RELOADED")

    @comms.command(name='l', hidden=True)
    @comms.is_owner()
    async def load_cog(self, ctx, cog):
        """
        Load a specific cog
        """
        printc('[...]: LOADING COGS')
        if cog in self.all_cogs:
            try:
                self.bot.load_extension(cog)
                self.cogs.append(cog)
                await ctx.send(duplicate(f'[ ! ]: COG {cog} HAS BEEN LOADED SUCCESSFULLY'), delete_after=10)
            except comms.ExtensionAlreadyLoaded:
                await ctx.send(f'Cog {cog} has already been loaded', delete_after=10)
            except Exception as e:
                printc(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            printc(f'WARNING: COG {cog} IS BLOCKED OR DOES NOT EXIST')

    @comms.command(name='u', hidden=True)
    @comms.is_owner()
    async def unload_cog(self, ctx, cog):
        """
        Unload a specific cog
        """
        if cog in self.all_cogs:
            try:
                self.bot.unload_extension(cog)
                self.cogs.pop(cog)
                await ctx.send(duplicate(f'[ ! ]: COG {cog} UNLOADED SUCCESSFULLY'), delete_after=10)
            except Exception as e:
                printc(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            await ctx.send(duplicate(f'WARNING: COG {cog} IS BLOCKED OR DOES NOT EXIST'), delete_after=10)

    @comms.command(name='exit', hidden=True)
    @comms.is_owner()
    async def logout(self, ctx):
        """
        Make the bot logout
        """
        printc(f'WARNING: LOGGING OUT...')
        await self.bot.logout()


"""

Function to pass objects into the main cog to run the bot

"""


def setup_bot(bot=comms.Bot(command_prefix='$', case_insensitive=True)):
    """
    Passing objects into the MainCog, then running the bot
    """
    # Searching for cogs within the cogs directory
    cogs = []
    for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
        cog = '.'.join(str(y) for y in dirpath[len(path()):].split('\\'))
        if '__pycache__' not in cog:
            cogs.extend([f'{cog}.{i[:-3]}' for i in filenames if i[:-3] not in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r').readlines()]])
    bot.add_cog(MainCog(bot, cogs))
    # Looping the input until token is correct
    checkToken = True
    while checkToken:
        try:
            token = json.load(open(path('relay', 'configuration', 'config.json')))['discord']
            bot.run(token, bot=True, reconnect=True)
            checkToken = False
        except FileNotFoundError:
            print('WARNING: TOKEN FILE NOT FOUND')
        except discord.errors.LoginFailure:
            print('WARNING: INCORRECT DISCORD TOKEN')


if __name__ == '__main__':
    setup_bot()
else:
    printc('WARNING: BOT CANNOT BE BOOTED FROM ANOTHER LOCATION')
