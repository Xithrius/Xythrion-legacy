"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools
import os
# import re

import discord
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from discord.ext import commands as comms
# from PIL import Image

from modules.output import file_name, path

plt.style.use('fast')


class Graphing(comms.Cog):
    """Graphing math items"""

    def __init__(self, bot):
        self.bot = bot

        sp.init_printing()

        self.equations = {
            'sin' = np.sin,
            'cos' = np.cos,
            'tan' = np.tan
        }

    """ Checks """

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    """ Cog-specific functions """

    def create_image(self, eq, r=[int]) -> str:
        for i, e in enumerate(eq, 1):
            if len(eq) > 1:
                plt.subplot(2, 1, i)

            # plt.plot(np.sin(np.linspace(0, 2 * np.pi)), markevery=1)
            arr = np.linspace(0, 5) # get this to work
            plt.plot(((arr ** 2) + arr))

            plt.xticks(rotation='vertical')
            plt.grid()
            plt.xlabel('x')
            plt.ylabel('y', rotation='horizontal')
            plt.title(e)
            plt.gcf().autofmt_xdate()

        p = path('tmp', f'{file_name()}.png')
        plt.savefig(p)
        plt.clf()

        return p

    """ Commands """

    @comms.command()
    async def graph(self, ctx, *, eq: str):
        func = functools.partial(self.create_image, eq.split())
        p = await self.bot.loop.run_in_executor(None, func)
        await ctx.send(file=discord.File(p))
        os.remove(p)

        # im = Image.open('dead_parrot.jpg') # Can be many different formats.
        # pix = im.load()
        # print im.size  # Get the width and hight of the image for iterating over
        # print pix[x,y]  # Get the RGBA Value of the a pixel of an image
        # pix[x,y] = value  # Set the RGBA Value of the image (tuple)
        # im.save('alive_parrot.png')  # Save the modified pixels as .png


def setup(bot):
    bot.add_cog(Graphing(bot))
