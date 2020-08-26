"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from xythrion.bot import Xythrion
from xythrion.extensions.meta.guilds import Guilds
from xythrion.extensions.meta.links import Links


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Guilds(bot))
    bot.add_cog(Links(bot))
