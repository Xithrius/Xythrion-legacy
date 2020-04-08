"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import os

import discord
import matplotlib.pyplot as plt
from discord.ext import commands as comms

from modules import gen_filename, path


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

    def create_plot(self) -> str:
        plt.clf()
        plt.plot([1, 2, 3, 4])
        # plt.legend()
        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
        return f

    """ Commands """

    @comms.command(enabled=False)
    async def graph(self, ctx, *, eq: str):
        """Graphing equations

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]graph x^2 + x

        """
        lock = asyncio.Lock()
        async with lock:
            f = await self.bot.loop.run_in_executor(None, self.create_plot)
            file = discord.File(path('tmp', f), filename=f)

        await ctx.send(file=file)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Graphing(bot))
