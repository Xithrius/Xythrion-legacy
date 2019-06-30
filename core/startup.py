"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import traceback
import os
import json

import discord
from discord.ext import commands as comms

from handlers.modules.output import path, now, printc, duplicate, sectional_print


class MainCog(comms.Cog):
    """ Essential parts for the working bot """

    def __init__(self, bot, info, cogs):
        """ Object(s):
        Bot
        Version info
        Extensions of the bot (mutable)
        Extensions of the bot (immutable)
        Background task for loading extensions in
        People who have permission for these commands
        """
        self.bot = bot
        self.info = info
        self.cogs = cogs
        self.all_cogs = cogs
        self.bg_task = self.bot.loop.create_task(self.load_extensions())
        self.owners = json.load(open(path('handlers', 'configuration', 'config.json')))['owners']

    """ Background tasks """

    async def load_extensions(self):
        """ Load the cogs in after the bot is ready """
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
                printc(f"[WARNING]: EXTENSION(S) COULD NOT BE LOADED:\n\t{', '.join(str(y) for y in broken_cogs)}")
            if len(loaded_cogs) > 0:
                printc(f"[ ! ]: EXTENSION(S) LOADED:")
                sectional_print(loaded_cogs)
            else:
                printc("[WARNING]: NO EXTENSIONS HAVE BEEN LOADED")

    """ Commands """

    @comms.command(name='r', hidden=True)
    async def reload_cogs(self, ctx):
        """ Reload all cog(s) """
        printc('\n[...]: RELOADING EXTENSION(S)\n')
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
            await ctx.send(duplicate(f"[WARNING]: EXTENSION(S) COULD NOT BE RELOADED:\n\t{', '.join(str(y) for y in broken_cogs)}"), delete_after=10)
        if len(loaded_cogs) > 0:
            printc(f"[ ! ]: EXTENSION(S) RELOADED:")
            sectional_print(loaded_cogs)
            await ctx.send('Cogs have been reloaded successfully', delete_after=10)
        else:
            printc("[WARNING]: NO EXTENSION(S) HAVE BEEN RELOADED")

    @comms.command(name='l', hidden=True)
    async def load_cog(self, ctx, cog):
        """ Load a specific cog """
        printc(f'[...]: LOADING EXTENSION {cog}')
        for i in self.all_cogs:
            cog_exists = False
            if cog in i:
                try:
                    self.bot.load_extension(cog)
                    self.cogs.append(cog)
                    await ctx.send(duplicate(f'[ ! ]: EXTENSION {cog} HAS BEEN LOADED SUCCESSFULLY'), delete_after=10)
                    cog_exists = True
                except comms.ExtensionAlreadyLoaded:
                    await ctx.send(f'[WARNING]: EXTENSION {cog} HAS ALREADY BEEN LOADED', delete_after=10)
                    cog_exists = True
                except Exception as e:
                    printc(f'{cog}: {type(e).__name__} - {e}\n')
                    cog_exists = True
        if not cog_exists:
            printc(f'[WARNING]: EXTENSION {cog} IS BLOCKED OR DOES NOT EXIST')

    @comms.command(name='u', hidden=True)
    async def unload_cog(self, ctx, cog):
        """ Unload a specific cog """
        if cog in self.all_cogs:
            try:
                self.bot.unload_extension(cog)
                self.cogs.pop(cog)
                await ctx.send(duplicate(f'[ ! ]: EXTENSION {cog} UNLOADED SUCCESSFULLY'), delete_after=10)
            except Exception as e:
                printc(f'{cog}: {type(e).__name__} - {e}\n')
        else:
            await ctx.send(duplicate(f'[WARNING]: EXTENSION {cog} IS BLOCKED OR DOES NOT EXIST'), delete_after=10)

    @comms.command()
    async def exit(self, ctx):
        """ Makes the bot logout, duh """
        printc('[WARNING]: CLIENT IS LOGGING OUT')
        await ctx.bot.logout()

    """ Events """

    @comms.Cog.listener()
    async def on_ready(self):
        """ Event activates when bot is ready for use """
        lines = [f'> [{now()}]',
                 f'Xiux v{self.info.__version__} by {self.info.__author__}',
                 self.info.__copyright__,
                 f'Logged in as: {self.bot.user}',
                 f'Client ID: {self.bot.user.id}']
        lines = [str(x) for x in lines]
        longest = max(map(len, lines))
        barrier = f"+{'-' * (longest + 4)}+"
        lines = '\n\t'.join(str(y) for y in [f'|  {x}{" " * (longest - len(x))}  |' for x in lines])
        print(f'\n\t{barrier}\n\t{lines}\n\t{barrier}\n')
        await self.bot.change_presence(activity=discord.Game(name='Visual Studio Code'))


def start(info):
    try:
        bot = comms.Bot(command_prefix='$', help_command=None)
        cogs = []
        config = json.load(open(path('handlers', 'configuration', 'config.json'), 'r'))
        for folder in os.listdir(path('cogs')):
            cogs.extend([f'cogs.{folder}.{x[:-3]}' for x in os.listdir(path('cogs', folder)) if x[:-3] not in config['blocked cogs']])
        bot.add_cog(MainCog(bot, info, cogs))
        bot.run(config['discord'], bot=True, reconnect=True)
    except discord.errors.LoginFailure:
        printc(f'[WARNING]: INCORRECT DISCORD TOKEN')
