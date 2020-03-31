"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from http.client import responses

from discord.ext import commands as comms


class Connections(comms.Cog):
    """Summary for Connections

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

    @comms.command(aliases=['status', 'response', 'code'])
    async def http_code(self, ctx, code: int):
        """Gets the http status code information.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            code (int): The status code that is wanted.

        """
        await ctx.send(f'{code} means {responses[int(code)]}')


def setup(bot):
    bot.add_cog(Connections(bot))
