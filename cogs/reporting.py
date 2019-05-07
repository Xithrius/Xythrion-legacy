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


from discord.ext import commands as comms
import discord

from relay.containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Template cog
# //////////////////////////////////////////////////////////////////////////// #
# Nothing to see here
# //////////////////////////////////////////////////////////////////////////// #


class BugCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.group()
    async def bug(self, ctx):
        """
        Reports a bug that the bot has
        """
        if ctx.invoked_subcommand is None:
            pass
        
    @bug.command()
    async def report(self, ctx):
        """

        """
        with open(path()) as f:
            pass


def setup(bot):
    bot.add_cog(BugCog(bot))
