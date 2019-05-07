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
# Twitter request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from Twitter
# //////////////////////////////////////////////////////////////////////////// #


class Twitter_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.group()
    async def twitter(self, ctx):
        """
        Twitter group command
        """
        if ctx.invoked_subcommand is None:
            pass

    @twitter.command()
    async def user(self, ctx):
        """
        Getting information about a twitter user
        """
        pass


def setup(bot):
    bot.add_cog(Twitter_Requester(bot))
