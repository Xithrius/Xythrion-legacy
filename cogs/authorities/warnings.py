"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms

from handlers.modules.output import printc


class WarningsCog(comms.Cog):
    """ Warn the owner about occurances """

    def __init__(self, bot):
        """ Objects:
        Bot
        """
        self.bot = bot

    """ Events """

    @comms.Cog.listener()
    async def on_disconnect(self):
        """ Sends warning when the client disconnects from the network """
        printc(f'[WARNING]: CLIENT HAS DISCONNECTED FROM NETWORK')

    @comms.Cog.listener()
    async def on_connect(self):
        """ Sends warning when the client connects to the network """
        printc(f'[WARNING]: CLIENT HAS CONNECTED TO NETWORK')

    @comms.Cog.listener()
    async def on_resumed(self):
        """ Sends warning when the client resumes a session """
        printc('[WARNING]: CLIENT HAS RESUMED CURRENT SESSION')


def setup(bot):
    bot.add_cog(WarningsCog(bot))
