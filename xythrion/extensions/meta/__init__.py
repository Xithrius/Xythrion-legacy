from discord.ext.commands import Bot
from xythrion.extensions.meta.guilds import Guilds
from xythrion.extensions.meta.links import Links


def setup(bot: Bot):
    """The necessary function for loading in cogs within this folder.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Guilds(bot))
    bot.add_cog(Links(bot))
