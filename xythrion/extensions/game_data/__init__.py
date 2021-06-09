from xythrion.bot import Xythrion
from xythrion.extensions.game_data.factorio import Factorio
from xythrion.extensions.game_data.warframe import Warframe


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Factorio(bot))
    bot.add_cog(Warframe(bot))
