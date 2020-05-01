"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import re
import typing as t
import traceback
import sys

import discord
import numpy as np
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import (
    embed_attachment, gen_filename, path, quick_block, parallel_executor
)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
except Exception as e:
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


class Graphing(comms.Cog):
    """Summary for Graphing

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific functions """

    @parallel_executor
    def parse_equation(self, eq: str, domain: list = None) -> t.Tuple[np.array]:
        eq = re.finditer(r'([\-\+])*(\s)*(\w)*(\^([\-\+])*\d)*', eq)
        eq = [y.group().replace(' ', '').split('^') for y in eq if not y.group().strip() == '']

        x = np.arange(*domain if domain else [-10, 10], 0.1)
        y = x

        for item in eq:
            if 'x' not in item[0]:
                y += int(item[0])

            else:
                try:
                    y *= int(item[0][:-1])
                except (IndexError, ValueError):
                    pass

                try:
                    y = pow(y, float(item[1]))
                except IndexError:
                    pass

        return x, y

    @parallel_executor
    def create_plot(self, lst: t.List[tuple]) -> str:
        plt.clf()

        for item in lst:
            x, y = item
            plt.plot(x, y)

        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f), format='png')
        return f

    """ Commands """

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command()
    async def graph(self, ctx, *, entry: str):
        """Graphing equations.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            eq (str): The equation to be parsed and graphed.

        Command examples:
            >>> [prefix]graph x^2 + x

        """
        domain = None

        try:
            domain = entry[entry.index('domain') + len('domain') + 1:]
            domain = [int(x.strip()) for x in domain.split(',')]
            E = entry[:entry.index('domain') - 1].strip()
        except ValueError:
            E = entry

        eq = [x.strip() for x in E.split(',')]

        lst = []

        for item in eq:
            try:
                x, y = await self.parse_equation(item, domain)
                lst.append((x, y))

            except (ValueError, IndexError):
                return await ctx.send(
                    '`The graph command only accepts polynomials with exponents and coefficients.`')
                break

        f = await self.create_plot(lst)

        embed = discord.Embed()
        file, embed = embed_attachment(path('tmp', f), embed)
        embed.description = await quick_block({'Equation': E, 'Domain': domain})

        await ctx.send(file=file, embed=embed)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Graphing(bot))
