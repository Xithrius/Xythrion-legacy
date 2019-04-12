'''

+----[ Demonically ]----------------------------+
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


import discord
from discord.ext import commands as comms

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class MemeCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////// # Commands
    @comms.command(name='poem')
    async def poem(self, ctx, string):
        pass


def setup(bot):
    bot.add_cog(MemeCog(bot))
