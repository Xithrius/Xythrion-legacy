"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands import Cog, Bot, Context


class Math(Cog):
    """Calculates equations and/or expressions.

    Attributes:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(aliases=['calc'], enabled=False)
    async def calculate(self, ctx: Context, *, ex: str) -> None:
        """Lexes and calculates the expression given by a user.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.
            ex (str): The expression to be lexed and calculated.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]calculate 2 + 2

        """
        pass
