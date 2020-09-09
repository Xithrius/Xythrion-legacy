from xythrion.bot import Xythrion
from xythrion.extensions.meta.dates import Dates
from xythrion.extensions.meta.guilds import Guilds
from xythrion.extensions.meta.help import Help
from xythrion.extensions.meta.links import Links


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Dates(bot))
    bot.add_cog(Guilds(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(Links(bot))
