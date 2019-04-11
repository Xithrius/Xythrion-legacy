'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import discord
from discord.ext import commands as comms
import imageio

# from essentials.pathing import path, mkdir


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class ModificationCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////// # Commands
    @comms.command()
    async def cli(self, ctx, infile, outfile, factor):
        vid = imageio.get_reader(infile, 'ffmpeg')

        fps = vid.get_meta_data()['fps']

        writer = imageio.get_writer(outfile, fps=fps)

        buildUp = factor

        for i, f in enumerate(vid):
            if buildUp >= factor:
                writer.append_data(f)
                buildUp -= factor
            buildUp += 1

        writer.close()


def setup(bot):
    bot.add_cog(ModificationCog(bot))
