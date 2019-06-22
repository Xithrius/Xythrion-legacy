'''
>> ARi0
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
import re

from discord.ext import commands as comms
import discord

from ARi0.containers.QOL.shortened import now
from ARi0.containers.QOL.pathing import path
from ARi0.containers.output.printer import printc


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
            `Command`: `$plot graph <equation> <x> <y>`
            `<equation>`: `ex. y=mx+b`
            `<x>`: `The window of the x domain ex. (1,1) or [1,1]`
            `<y>`: `The window of the y range ex. (1,1) or [1,1]`
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @custom_plot.command()
    async def graphing(self, ctx, equation, x, y):
        print(ctx.message.content)
        m = re.findall(r'(\((.*)\))|(\[(.*)\])', ctx.message.content)
        x, y = m[0][1].replace(' ', ''), m[1][-1].replace(' ', '')
        plt.plot(x, y)
        plt.savefig(path('tmp', 'plots', 'plot.png'))
        # embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(file=discord.File(path('tmp', 'plots', 'plot.png')))
        embed = discord.Embed(title=f'`{equation}`', colour=0xc27c0e, timestamp=now())


def setup(bot):
    bot.add_cog(Plot_Requester(bot))
