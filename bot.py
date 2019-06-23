'''
>> ARi0
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import traceback
import json
import os
import sys

import discord
from discord.ext import commands as comms

from ARi0.containers.QOL.pathing import path
from ARi0.containers.output.printer import duplicate, printc, sectional_print
from ARi0.containers.QOL.shortened import now
import ARi0


# //////////////////////////////////////////////////////////////////////////// #
# Main cog                                                                     #
# //////////////////////////////////////////////////////////////////////////// #
# Essential parts for the working bot                                          #
# //////////////////////////////////////////////////////////////////////////// #


class MainCog(comms.Cog):

    def __init__(self, bot, cogs):
        """ Object(s):
        Bot
        Extensions of the bot (mutable)
        Extensions of the bot (immutable)
        Background task for loading extensions in
        """
        self.bot = bot
        self.cogs = cogs
        self.all_cogs = cogs
        self.bg_task = self.bot.loop.create_task(self.load_extensions())

    """

    Background tasks

    """
    async def load_extensions(self):
        """
        Load the cogs in after the bot is ready
        """
        printc('[...]: LOADING EXTENSION(S)')
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
                printc(f"WARNING: EXTENSION(S) COULD NOT BE LOADED:\n\t{', '.join(str(y) for y in broken_cogs)}")
            if len(loaded_cogs) > 0:
                printc(f"[ ! ]: EXTENSION(S) LOADED:")
                sectional_print(loaded_cogs)
            else:
                printc("WARNING: NO EXTENSIONS HAVE BEEN LOADED")

    """

    Commands

    """
    @comms.command(name='r', hidden=True)
    @comms.is_owner()
    async def reload_cogs(self, ctx):
        """
        Reload all cog
        """
        print(f'\n{"[" * 8} [ RELOADING ] {"]" * 8}\n')
        # printc('[...]: RELOADING EXTENSION(S)')
        loaded_cogs, broken_cogs = [], []
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
            await ctx.send(duplicate(f"WARNING: EXTENSION(S) COULD NOT BE RELOADED:\n\t{', '.join(str(y) for y in broken_cogs)}"), delete_after=10)
        if len(loaded_cogs) > 0:
            printc(f"[ ! ]: EXTENSION(S) RELOADED:")
            sectional_print(loaded_cogs)
            await ctx.send('Cogs have been reloaded successfully', delete_after=10)
        else:
            printc(f"WARNING: NO EXTENSION(S) HAVE BEEN RELOADED")

    @comms.command(name='l', hidden=True)
    @comms.is_owner()
    async def load_cog(self, ctx, cog):
        """
        Load a specific cog
        """
        printc('[...]: LOADING EXTENSION(S)')
        for i in self.all_cogs:
            cog_exists = False
            if cog in i:
                try:
                    self.bot.load_extension(cog)
                    self.cogs.append(cog)
                    await ctx.send(duplicate(f'[ ! ]: Extension {cog} HAS BEEN LOADED SUCCESSFULLY'), delete_after=10)
                    cog_exists = True
                except comms.ExtensionAlreadyLoaded:
                    await ctx.send(f'EXTENSION {cog} HAS ALREADY BEEN LOADED', delete_after=10)
                    cog_exists = True
                except Exception as e:
                    printc(f'{cog}: {type(e).__name__} - {e}\n')
                    cog_exists = True
        if not cog_exists:
            printc(f'WARNING: EXTENSION {cog} IS BLOCKED OR DOES NOT EXIST')

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
                await ctx.send(duplicate(f'[ ! ]: EXTENSION {cog} UNLOADED SUCCESSFULLY'), delete_after=10)
            except Exception as e:
                printc(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            await ctx.send(duplicate(f'WARNING: EXTENSION {cog} IS BLOCKED OR DOES NOT EXIST'), delete_after=10)

    @comms.command()
    @comms.is_owner()
    async def exit(self, ctx):
        """
        Destroys everything when exiting
        """
        printc('WARNING: CLIENT IS LOGGING OUT')
        await ctx.bot.logout()

    """

    Events

    """
    @comms.Cog.listener()
    async def on_ready(self):
        """
        Event activates when bot is ready for use
        """
        lines = [f'> [{now()}]',
                 f'ARi0.py v{ARi0.__version__}',
                 f'Logged in as: {self.bot.user}',
                 f'Client ID: {self.bot.user.id}']
        longest = max(map(len, lines))
        barrier = f"+{'-' * (longest + 4)}+"
        lines = '\n\t'.join(str(y) for y in [f'|  {x}{" " * (longest - len(x))}  |' for x in lines])
        print(f'\n\t{barrier}\n\t{lines}\n\t{barrier}\n')

if __name__ == '__main__':
    try:
        bot = comms.Bot(command_prefix='$', help_command=None, case_insensitive=True)
        cogs = []
        for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
            cog = '.'.join(str(y) for y in dirpath[len(path()):].split('\\'))
            if '__pycache__' not in cog.split('.'):
                cogs.extend([f'{cog}.{i[:-3]}' for i in filenames if i[:-3] not in [x[:-1] for x in open(path('ARi0', 'configuration', 'blocked_cogs.txt'), 'r').readlines()]])
        bot.add_cog(MainCog(bot, cogs))
        bot.run(json.load(open(path('ARi0', 'configuration', 'config.json')))[
                'discord'], bot=True, reconnect=True)
    except discord.errors.LoginFailure as e:
        printc(f'WARNING: {e}')
