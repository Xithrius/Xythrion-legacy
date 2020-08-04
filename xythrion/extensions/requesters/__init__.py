from discord.ext.commands import Bot
from xythrion.extensions.requesters.cats import Cats
from xythrion.extensions.requesters.reddit import Reddit


def setup(bot: Bot):
    """The necessary function for loading in cogs within this folder.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Reddit(bot))
    bot.add_cog(Cats(bot))
