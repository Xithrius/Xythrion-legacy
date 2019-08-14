"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


class Interactions_Director(comms.Cog):
    """ Director for interactions """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.message.author.id in self.bot.owner_ids

    """ Events """

    @comms.Cog.listener()
    async def interactions_event(self):
        """ """
        pass

    """ Commands """

    @comms.command()
    async def interactions_command(self, ctx):
        """ """
        pass


def setup(bot):
    bot.add_cog(Interactions_Director(bot))
