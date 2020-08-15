from xythrion.bot import Xythrion
from xythrion.extensions.requesters.reddit import Reddit


def setup(bot: Xythrion):
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Reddit(bot))
