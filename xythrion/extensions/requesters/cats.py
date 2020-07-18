"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord

from xythrion.utils import http_get, markdown_link
from http import HTTPStatus


class Cats(comms.Cog):
    """A large amount of cats.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.command(aliases=['status', 'response', 'code', 'statuscat'])
    async def http_cat(self, ctx, code: int):
        """Gets the http status code information.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            code (int): The status code that is wanted.

        Command examples:
            >>> [prefix]http_cat 404
            >>> [prefix]status 200
            >>> [prefix]response_code 400

        """
        embed = discord.Embed(title=f'**Status: {code}**')
        embed.set_image(url=f'https://http.cat/{code}.jpg')

        try:
            HTTPStatus(code)

        except ValueError:
            embed.set_footer(text='Inputted status code does not exist.')

        await ctx.send(embed=embed)

    @comms.command()
    async def neko(self, ctx):
        """Returns a 'neko' (human cat-girl, not actual cat) image.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]neko

        """
        url = await http_get('https://nekos.life/api/v2/img/neko', session=self.bot.session)
        embed = discord.Embed(description=markdown_link('Image url', url['url']))

        embed.set_image(url=url['url'])
        embed.set_footer(text='Taken from https://nekos.life/')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Cats(bot))
