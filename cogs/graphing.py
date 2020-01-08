"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools
import re

from discord.ext import commands as comms
import discord

from modules.output import path, file_name


class Graphing(comms.Cog):
    """Graphing math items"""

    def __init__(self, bot):
        self.bot = bot

    """ Cog-specific functions """

    def create_latex_polynomial():
        pass

    """ Commands """

    @comms.command()
    async def graph(self, ctx, *, eq: str):
        pass

        # func = functools.partial(parse_polynomial, one, two, three=3)
        # some_stuff = await bot.loop.run_in_executor(None, thing)
        # from PIL import Image

        # im = Image.open('dead_parrot.jpg') # Can be many different formats.
        # pix = im.load()
        # print im.size  # Get the width and hight of the image for iterating over
        # print pix[x,y]  # Get the RGBA Value of the a pixel of an image
        # pix[x,y] = value  # Set the RGBA Value of the image (tuple)
        # im.save('alive_parrot.png')  # Save the modified pixels as .png


def setup(bot):
    bot.add_cog(Graphing(bot))
