"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord


class Math(comms.Cog):
    """Calculaing simple equations that are parsed with regex.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(name='math', aliases=['calculate'])
    async def _math(self, ctx, *, ex: str):
        """Calculating expressions.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            ex (str): The expression to be parsed, and calculated.

        """
        pass


def setup(bot):
    bot.add_cog(Math(bot))
