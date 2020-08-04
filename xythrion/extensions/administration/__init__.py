from discord.ext.commands import Bot
from xythrion.extensions.administration.moderation import Moderation
from xythrion.extensions.administration.warnings import Warnings


def setup(bot: Bot):
    """The necessary function for loading in cogs within this folder.

    Args:
        bot (:obj:`discord.ext.commands.Bot`): Represents a Discord bot.

    Returns:
        :obj:`type(None)`: Always None

    """
    bot.add_cog(Moderation(bot))
    bot.add_cog(Warnings(bot))
