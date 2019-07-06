"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import json
import sqlite3

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

        self.add_command(self.reload_cogs)
        # self.add_command(self.load_cog)
        # self.add_command(self.unload_cog)

    """ Database checking, before startup """

    def db_checks(self):
        """ """
        for db in os.listdir(path('repository', 'database')):
            try:
                conn = sqlite3.connect(path('repository', 'database', db))
                conn.close()

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.author.id in ctx.bot.config.owners

    """ Commands """

    @comms.command(name='r')
    async def reload(self, ctx):
        pass

    """ Events """

    async def on_ready(self):
        """ Extensions are loaded as quickly as possible """
        printc('[. . .]: LOADING EXTENSION(S)')
        self.cogs = []
        blocked_cogs = json.load(open(path('handlers', 'configuration', 'config.json'), 'r'))['blocked cogs']
        for folder in os.listdir(path('cogs')):
            self.cogs.extend([f'cogs.{folder}.{cog[:-3]}' for cog in os.listdir(path('cogs', folder)) if cog[:-3] not in ['__pycach', *blocked_cogs]])
        cog_amount = len(cogs)
        broken_cogs = []
        loaded_cogs = 0
        progress_bar(0, cog_amount)
        for i, cog in enumerate(self.cogs):
            try:
                self.load_extension(cog)
                progress_bar(i + 1, cog_amount)
            except Exception as e:
                broken_cogs.append([cog, e])


    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        printc('[WARNING]: BOT HAS DISCONNECTED FROM NETWORK')

    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        printc('[WARNING]: BOT HAS CONNECTED TO NETWORK')

    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        printc('[WARNING]: BOT HAS RESUMED CURRENT SESSION')


if __name__ == "__main__":
    xiux = XiuxBot(command_prefix='.', help_command=None)
