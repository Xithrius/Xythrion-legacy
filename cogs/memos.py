'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


from discord.ext import commands as comms


# ///////////////////////////////////////////////////////// #
# Memo cog
# ////////////////////////
# Cog for reminding people of things that aren't stocks
# ///////////////////////////////////////////////////////// #


class MemosCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    async def nothing(self, ctx):
        ctx.send('nothing here yet')


def setup(bot):
    bot.add_cog(MemosCog(bot))
