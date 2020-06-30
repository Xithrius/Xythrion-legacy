"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from xythrion.utils import tokenization


class Math(comms.Cog):
    """Calculates equations and/or expressions.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command()
    async def calculate(self, ctx: comms.Context, *, msg: str) -> None:
        pass


def setup(bot: comms.Bot) -> None:
    """The necessary function for loading in cogs within this file.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Math(bot))
