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

    async def parse_equation(self, eq: str) -> t.List[t.List[int]]:
        eq = re.finditer(r'([\-\+])*(\s)*(\w)*(\^\d)*', eq)
        eq = [y.group() for y in eq if not y.group().strip() == '']
        return eq

    def create_plot(self) -> str:
        plt.clf()

        # start, stop, step
        x = np.arange(0, 4 * np.pi, 0.1)
        y = np.sin(x)
        plt.plot(x, y)

        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
        return f

    """ Commands """

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command()
    async def graph(self, ctx, *, eq: str):
        """Graphing equations.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]graph x^2 + x

        """
        eq = await self.parse_equation(eq)
        f = await lock_executor(self.create_plot, eq, loop=self.bot.loop)
        embed = discord.Embed(title=ast('A graph:'))
        file, embed = embed_attachment(path('tmp', f), embed)

        await ctx.send(file=file, embed=embed)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Graphing(bot))
