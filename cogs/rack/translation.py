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
# Converter: Language
# /////////////////////////////////////////////////////////
# A cog that encrypts and decrypts different languages
# //////////////////////////////////////////////////////////////////////////// #


class Language_Converter(comms.Cog):

    def __init__(self, bot):
        """ Object(s): bot and background task(s) """
        self.bot = bot

# //////////////////////////////////////////////// # Commands


def setup(bot):
    bot.add_cog(Language_Converter(bot))
