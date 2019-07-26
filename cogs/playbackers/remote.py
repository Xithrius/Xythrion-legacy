"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord

from handlers.modules.output import path, printc, now


class Remote_Playbacker(comms.Cog):
    """ Playbacker for remote """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task loop creation
        """
        self.bot = bot

        self._loader = self.bot.loop.create_task(self.load_remote())

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self._loader.cancel()

    """ Background tasks """

    async def load_remote(self):
        """ """
        pass

    """ Events """

    @comms.Cog.listener()
    async def remote_event(self):
        """ """
        pass

    """ Commands """

    @comms.command()
    async def remote_command(self, ctx):
        """ """
        pass


def setup(bot):
    bot.add_cog(Remote_Playbacker(bot))
