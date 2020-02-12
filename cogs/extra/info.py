"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Info(comms.Cog):
    """ """

    def __init__(self, bot):
        """ """
        self.bot = bot

    @comms.command(aliases=['runtime'])
    async def uptime(self, ctx):
        """ """
        d = abs(self.bot.startup_time - datetime.datetime.now())
        info = {
            'Date of startup:': self.bot.startup_time,
            'Time since startup': d
        }
        embed = discord.Embed(description=f'Up since `{self.bot.startup_time}` (`{d}`)')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
