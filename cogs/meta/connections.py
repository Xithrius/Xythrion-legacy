"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


# from http.client import responses

import discord
from discord.ext import commands as comms

from modules import ast


class Connections(comms.Cog):
    """Giving information about response codes.

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
    async def response_code(self, ctx, code: int):
        """Gets the http status code information.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            code (int): The status code that is wanted.

        Command examples:
            >>> [prefix]status 200
            >>> [prefix]response_code 400

        """
        embed = discord.Embed(
            title=ast(f'Status {code}:')
            # description=f'`{responses[int(code)]}`' <- if http.cat ever dies (hopefully never).
        )
        embed.set_image(url=f'https://http.cat/{code}.jpg')
        embed.set_footer(text=f'Taken from https://http.cat/')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Connections(bot))
