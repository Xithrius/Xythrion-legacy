from xythrion.bot import Xythrion
from xythrion.extensions.meta.dates import Dates
from xythrion.extensions.meta.links import Links
from xythrion.extensions.meta.notes import Notes
from xythrion.extensions.meta.snippets import Snippets


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Dates(bot))
    bot.add_cog(Links(bot))
    bot.add_cog(Notes(bot))
    bot.add_cog(Snippets(bot))
