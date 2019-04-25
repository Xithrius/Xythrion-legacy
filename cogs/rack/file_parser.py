'''

+----[ Demoness ]-------------------------------+
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


import asyncio

from discord.ext import commands as comms
# import discord

# from containers


# //////////////////////////////////////////////////////////////////////////// #
# Parser: Files
# /////////////////////////////////////////////////////////
# A cog specifically for parsing files
# //////////////////////////////////////////////////////////////////////////// #


class Paser_File(comms.Cog):

    def __init__(self, bot):
        """ Object(s): bot and background task(s) """
        self.bot = bot


def setup(bot):
    bot.add_cog(Paser_File(bot))
