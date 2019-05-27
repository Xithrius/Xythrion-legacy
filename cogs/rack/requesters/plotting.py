'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Plotting request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get a graph given parameters
# //////////////////////////////////////////////////////////////////////////// #


class Plot_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.group(name='plot')
    async def custom_plot(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='`Usage of the plot command`', colour=0xc27c0e, timestamp=now())
            help = '''
            `Command`: `$plot graph <equation> <domain> <range>`
            `<equation>`: ``
            `<domain>`: ``
            `<range>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @custom_plot.command()
    async def graphing(self, ctx, *args):
        x = np.linspace(0, 10)
        y = np.exp(x)
        plt.plot(x, y)
        plt.savefig(path('tmp', 'plots', 'plot.png'))
        # embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(file=discord.File(path('tmp', 'plots', 'plot.png')))


def setup(bot):
    bot.add_cog(Plot_Requester(bot))
