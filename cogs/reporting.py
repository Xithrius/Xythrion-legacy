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
    async def bug(self, ctx):
        """
        Description
        """
        await ctx.send('Not ready')


def setup(bot):
    bot.add_cog(BugCog(bot))
