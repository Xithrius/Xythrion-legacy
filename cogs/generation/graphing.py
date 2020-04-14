"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import typing as t
import re

import discord
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import ast, embed_attachment, gen_filename, lock_executor, path

plt.style.use('dark_background')


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

    async def parse_eqation(self, eq: str, domain: list = None) -> t.Tuple[np.array]:
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

    def create_plot(self, x, y, grid: bool) -> str:
        plt.clf()
        plt.plot(x, y)
        if grid:
            plt.grid()

        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
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
        options = {'domain': False, 'grid': False}

        eq = entry
        for item in [x for x in options.keys() if x in entry]:
            eq = entry[:entry.index(item)]
            tmp = entry[entry.index(item) + len(item) + 1:]

            try:
                options[item] = [int(x.strip()) for x in tmp.split(',')]
            except ValueError:
                options[item] = int(tmp)

        print(options)
        print(eq)

        try:
            x, y = await self.parse_eqation(eq, options['domain'])
        except Exception:
            return await ctx.send(
                '`The graph command only accepts polynomials with exponents and coefficients.`')
        f = await lock_executor(self.create_plot, (x, y, options['grid']))
        embed = discord.Embed(title=ast(f'The graph of "{eq}":'))
        file, embed = embed_attachment(path('tmp', f), embed)

        await ctx.send(file=file, embed=embed)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Graphing(bot))
