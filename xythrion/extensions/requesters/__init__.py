from xythrion.bot import Xythrion
from xythrion.extensions.requesters.api_usage import APIUsage
from xythrion.extensions.requesters.reddit import Reddit


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(APIUsage(bot))
    bot.add_cog(Reddit(bot))
