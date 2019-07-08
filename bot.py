"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import collections
import sqlite3
import json
import os
import pickle

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, now, printc, sectional_print, progress_bar


class XiuxBot(comms.Bot):
    """ """

    def __init__(self, *args, **kwargs):
        """ Securing before safely starting the bot """
        super().__init__(*args, **kwargs)

        if self.db_checks():
            pass

        self.getAttributes()

    """ Adding attributes """

    def getAttributes(self):
        """ """
        with open(path('handlers', 'configuration', 'config.json'), "r", encoding="utf8") as f:
            data = json.dumps(json.load(f))
            self.config = json.loads(data, object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))

    """ Database checking, before startup """

    def db_checks(self):
        """ """
        for db in os.listdir(path('repository', 'database')):
            try:
                conn = sqlite3.connect(path('repository', 'database', db))
                conn.close()
            except Exception as e:
                printc('')

    """ Events """

    async def on_ready(self):
        """ Extensions are loaded as quickly as possible """
        printc('[. . .]: LOADING EXTENSION(S)')
        self.extensions = {}
        for folder in os.listdir(path('cogs')):
            self.extensions['folder'] = [cog for cog in os.listdir(path('cogs', folder)) if cog[:-3] not in ['__pycach', *self.config.blocked_cogs]]
        self.attached_extensions = [f'cogs.{k}.{v}' for k, v in self.extensions.items()]
        cog_amount = len(self.attached_extensions)
        broken_cogs = []
        loaded_cogs = 0
        progress_bar(0, cog_amount)
        for i, cog in enumerate(self.attached_extensions):
            try:
                self.load_extension(cog)
                progress_bar(i + 1, cog_amount)
            except Exception as e:
                broken_cogs.append([cog, e])

    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        printc('[WARNING]: CLIENT HAS DISCONNECTED FROM NETWORK')

    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        printc('[WARNING]: CLIENT HAS CONNECTED TO NETWORK')

    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        printc('[WARNING]: CLIENT HAS RESUMED CURRENT SESSION')


class MainCog(comms.Cog):
    """ """

    def __init__(self, bot):
        """ Objects:
        Xiux(comms.Bot) as a class attribute
        """
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.config.owners

    """ Commands """

    @comms.command(name='r')
    async def reload_cog(self, ctx, cog=False):
        if not cog:
            pass
        else:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                pass

    @comms.command(name='l')
    async def unload_cog(self, ctx, cog: str):
        pass

    @comms.command(name='u')
    async def load_cog(self, ctx, cog: str):
        pass

    @comms.command()
    async def exit(self, ctx):
        """ Makes the client logout """
        printc('[WARNING]: CLIENT IS LOGGING OUT')
        await ctx.bot.logout()


if __name__ == "__main__":
    xiux = XiuxBot(command_prefix='.', help_command=None)
    xiux.run(xiux.config.discord, bot=True, reconnect=True)
