from xythrion.bot import Xythrion
from xythrion.extensions.generation.fractals import Fractals
from xythrion.extensions.generation.graphing import Graphing
from xythrion.extensions.generation.math import Math
from xythrion.extensions.generation.qrcode import QRCode
from xythrion.extensions.generation.randoms import Randoms


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Fractals(bot))
    bot.add_cog(Graphing(bot))
    bot.add_cog(Math(bot))
    bot.add_cog(QRCode(bot))
    bot.add_cog(Randoms(bot))
