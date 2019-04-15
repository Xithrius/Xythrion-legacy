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


from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
# Meme cog
# /////////////////////////////////////////////////////////
# Gets user input memes, and then returns when called for
# //////////////////////////////////////////////////////////////////////////// #


class MemeCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Fetch a poem from the folder of poems
    @comms.command(name='poem')
    async def poem(self, ctx, string):
        pass


def setup(bot):
    bot.add_cog(MemeCog(bot))
