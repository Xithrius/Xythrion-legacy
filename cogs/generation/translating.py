"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms


class Translating(comms.Cog):
    """Translating from English to different bases.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Commands """

    @comms.command(enabled=False)
    async def binary(self, ctx, *, msg: int):
        """Translates from integers to binary numbers.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            msg (int): A message containing only integers to be translated to binary.

        Command examples:
            >>> [prefix]binary 54238702453

        """
        await ctx.send(f'`{bin(msg)[2:]}`')


def setup(bot):
    bot.add_cog(Translating(bot))
