from xythrion.bot import Xythrion
from xythrion.extensions.meta.guilds import Guilds
from xythrion.extensions.meta.links import Links


def setup(bot: Xythrion):
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Guilds(bot))
    bot.add_cog(Links(bot))
