from xythrion.bot import Xythrion
from xythrion.extensions.generation.plotting import Plotting
from xythrion.extensions.generation.randoms import Randoms


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Plotting(bot))
    bot.add_cog(Randoms(bot))
