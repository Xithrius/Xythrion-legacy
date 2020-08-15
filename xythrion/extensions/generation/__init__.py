from xythrion.bot import Xythrion
from xythrion.extensions.generation.graphing import Graphing
from xythrion.extensions.generation.math import Math
from xythrion.extensions.generation.randoms import Randoms


def setup(bot: Xythrion):
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Graphing(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(Randoms(bot))
