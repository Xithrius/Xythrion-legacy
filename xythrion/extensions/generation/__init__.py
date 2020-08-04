from discord.ext.commands import Bot
from xythrion.extensions.generation.graphing import Graphing
from xythrion.extensions.generation.math import Math
from xythrion.extensions.generation.randoms import Randoms


def setup(bot: Bot):
    """The necessary function for loading in cogs within this folder.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Graphing(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(Randoms(bot))
