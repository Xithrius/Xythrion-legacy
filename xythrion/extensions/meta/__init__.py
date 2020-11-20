from xythrion.bot import Xythrion
from xythrion.extensions.meta.links import Links
from xythrion.extensions.meta.source import Source


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Links(bot))
    bot.add_cog(Source(bot))
