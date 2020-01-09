"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools
import re

import discord
import matplotlib.pyplot as plt
import sympy as sp
from discord.ext import commands as comms
from PIL import Image

from modules.output import file_name, path


class Graphing(comms.Cog):
    """Graphing math items"""

    def __init__(self, bot):
        self.bot = bot
        
        sp.init_printing()

    """ Cog-specific functions """

    def create_polynomial_info(self) -> str:
        pass

    """ Commands """

    @comms.command()
    async def graph(self, ctx, *, eq: str):
        func = functools.partial(self.create_polynomial_info)
        image_path = await self.bot.loop.run_in_executor(None, func)


        # im = Image.open('dead_parrot.jpg') # Can be many different formats.
        # pix = im.load()
        # print im.size  # Get the width and hight of the image for iterating over
        # print pix[x,y]  # Get the RGBA Value of the a pixel of an image
        # pix[x,y] = value  # Set the RGBA Value of the image (tuple)
        # im.save('alive_parrot.png')  # Save the modified pixels as .png


def setup(bot):
    bot.add_cog(Graphing(bot))
