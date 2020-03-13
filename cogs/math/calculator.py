"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord


class Calculator(comms.Cog):
    """Summary for Calculator

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(enabled=False)
    async def zeroes(self, ctx, *, eq: str):
        """Find the zeroes of a polynomial

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            eq (str): The equation to be parsed.

        """
        pass


def setup(bot):
    bot.add_cog(Calculator(bot))
