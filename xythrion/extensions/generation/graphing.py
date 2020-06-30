"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
# from pathlib import Path


class Graphing(comms.Cog):
    """Parsing a user's input and making a graph out of it..

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Commands """

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command(enabled=False)
    async def graph(self, ctx: comms.Context, *, entry: str) -> None:
        """Graphing equations.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            eq (str): The equation to be parsed and graphed.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]graph x^2 + x

        """
        # NOTE: Will be filled in once parsing utility is finished.
        pass

    # @comms.command()
    # async def path_test(self, ctx):
    #     print(Path.cwd() / 'tmp')


def setup(bot: comms.Bot) -> None:
    """The necessary function for loading in cogs within this file.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Graphing(bot))
