'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from discord.ext import commands as comms

from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Warnings cog
# //////////////////////////////////////////////////////////////////////////// #
# Warn the owner about everything bad that occurs
# //////////////////////////////////////////////////////////////////////////// #


class WarningsCog(comms.Cog):

    def __init__(self, bot):
        """ Objects:
        Bot
        """
        self.bot = bot

    """

    Events

    """
    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Sends error to the user
        """
        await ctx.send(error)
        printc(f'WARNING: {ctx.message.author} HAS CAUSED ERROR:\n\t{ctx.message.content}\n\t{error}')

    @comms.Cog.listener()
    async def on_disconnect(self):
        """
        Sends warning when the client disconnects from the network
        """
        printc(f'WARNING: CLIENT HAS DISCONNECTED FROM NETWORK')

    @comms.Cog.listener()
    async def on_connect(self):
        """
        Sends warning when the client connects to the network
        """
        printc(f'WARNING: CLIENT HAS CONNECTED TO NETWORK')

    @comms.Cog.listener()
    async def on_resumed(self):
        """
        Sends warning when the client resumes a session
        """
        printc('WARNING: CLIENT HAS RESUMED CURRENT SESSION')


def setup(bot):
    bot.add_cog(WarningsCog(bot))
