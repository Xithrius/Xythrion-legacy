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
# Translation cog
# /////////////////////////////////////////////////////////
# Translating into different languages
# //////////////////////////////////////////////////////////////////////////// #


class TranslationCog(comms.Cog):

    # //////////////////////// # Object(s): bot
    def __init__(self, bot):
        self.bot = bot


# //////////////////////////////////////////////// # Commands
    # //////////////////////// # English to binary
    @comms.command(name='binary')
    async def to_binary(self, ctx):
        ctx.send(f'')


def setup(bot):
    bot.add_cog(TranslationCog(bot))
