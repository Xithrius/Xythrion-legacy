from xythrion.bot import Xythrion
from xythrion.extensions.requesters.documentation import Documentation
from xythrion.extensions.requesters.reddit import Reddit
from xythrion.extensions.requesters.tinyy import Tinyy
from xythrion.extensions.requesters.weather import Weather


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Documentation(bot))
    bot.add_cog(Reddit(bot))
    bot.add_cog(Weather(bot))
    bot.add_cog(Tinyy(bot))
