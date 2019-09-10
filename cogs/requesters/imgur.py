"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * Nothing

"""

from discord.ext import commands as comms
import discord

from modules.output import path, ds


class Imgur_Requester(comms.Cog):
    """Fetching information from Imgur"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """Commands are only passed if the service is available

        Returns:
            True or False depending on the availability of the service

        """
        return self.bot.requester_status['imgur']

    """ Commands """

    @comms.group()
    async def imgur(self, ctx):
        """The Imgur group command for commands that are Imgur related.

        Returns:
            The built-in help command if no group command is passed

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **;help {ctx.command}** for help')

    @imgur.command()
    async def image(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Imgur_Requester(bot))
