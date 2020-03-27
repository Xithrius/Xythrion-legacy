"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms


class UNO(comms.Cog):
    """Summary for UNO

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command()
    async def uno(self, ctx):
        """Plays a move in uno

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        """


def setup(bot):
    bot.add_cog(UNO(bot))
