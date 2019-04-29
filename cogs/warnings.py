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


import sys
import datetime

from discord.ext import commands as comms

from containers.essentials.pathing import path, mkdir
from containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Warnings cog
# //////////////////////////////////////////////////////////////////////////// #
# Warn the owner about everything bad that occurs
# //////////////////////////////////////////////////////////////////////////// #


class WarningsCog(comms.Cog):

    def __init__(self, bot):
        """ Objects:
        Bot
        """
        self.bot = bot

    """

    Events

    """
    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Sends error to the user
        """
        await ctx.send(error)
        printc(f'WARNING: {ctx.message.author} HAS CAUSED ERROR:\n\t{ctx.message.content}\n\t{error}')

    @comms.Cog.listener()
    async def on_disconnect(self):
        """
        Sends warning when the client disconnects from the network
        """
        printc(f'WARNING: CLIENT HAS DISCONNECTED FROM NETWORK')

    @comms.Cog.listener()
    async def on_connect(self):
        """
        Sends warning when the client connects to the network
        """
        printc(f'WARNING: CLIENT HAS CONNECTED TO NETWORK')

    @comms.Cog.listener()
    async def on_resumed(self):
        """
        Sends warning when the client resumes a session
        """
        printc(f'WARNING: CLIENT HAS RESUMED CURRENT SESSION')

    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Sends warning when there's an update in the status of a member
        """
        pass

    @comms.Cog.listener()
    async def on_message(self, message):
        """
        Tracking, blocking, and removing files
        """
        try:
            if sys.argv[1] == 'log':
                now = datetime.datetime.now()
                check = True
                while check:
                    try:
                        with open(path('logs', message.guild, message.channel, f'{message.author}.txt'), 'a') as f:
                            f.write(f"[{now}]: '{message.content}'\n")
                            check = False
                    except FileNotFoundError:
                        mkdir('logs', message.guild, message.channel)
        except IndexError:
            pass


def setup(bot):
    bot.add_cog(WarningsCog(bot))