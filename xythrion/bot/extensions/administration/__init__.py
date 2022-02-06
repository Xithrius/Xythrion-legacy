from bot import Xythrion
from bot.extensions.administration.development import Development
from bot.extensions.administration.warnings import Warnings


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in extensions within this folder."""
    bot.add_cog(Development(bot))
    bot.add_cog(Warnings(bot))
