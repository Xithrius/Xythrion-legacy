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


import platform
import datetime
import os

from discord.ext import commands as comms
import discord

from relay.containers.QOL.pathing import path, mkdir
from relay.containers.QOL.shortened import now
from relay.containers.QOL.shortened import index_days
from relay.containers.output.printer import printc
from relay.containers.scraping.yahoo_finance import get_stock_summary
from relay.containers.permissions import tracker


# //////////////////////////////////////////////////////////////////////////// #
# Stock cog
# //////////////////////////////////////////////////////////////////////////// #
# Web scraping the internet for stock information
# //////////////////////////////////////////////////////////////////////////// #


class Stock_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_stock_reminders())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.bg_task.cancel()

    """

    Commands

    """
    @comms.command(name='stocks')
    async def get_current_stocks(self, ctx, abbreviation, option='low'):
        """ Get information about inputted stock """
        pass

    """

    Background tasks
    
    """
    async def check_stock_reminders(self):
        """
        Checks for requested reminders
        """
        pass



def setup(bot):
    bot.add_cog(Stock_Requester(bot))
