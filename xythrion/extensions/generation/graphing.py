"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Cog, Bot, Context


class Graphing(Cog):
    """Parsing a user's input and making a graph out of it..

    Attributes:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Commands """

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command(enabled=False)
    async def graph(self, ctx: Context, *, entry: str) -> None:
        """Lexing then Graphing equations that the user gives.

        Args:
            ctx (:obj:`discord.ext.commands.Context`):
                Represents the context in which a command is being invoked under.
            eq (str): The equation to be lexed and graphed.

        Returns:
            :obj:`type(None)`: Always None

        Command examples:
            >>> [prefix]graph x^2 + x

        """
        # NOTE: Will be filled in once lexer utility is finished.
        pass
