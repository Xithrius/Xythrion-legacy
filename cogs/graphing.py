"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


class Graphing(comms.Cog):
    """"""

    def __init__(self, bot):

        self.bot = bot

    @comms.group()
    async def graph(self):
        pass

    @graph.command()
    async def zeros(self, ctx, *, eq: str):
        pass


def setup(bot):
    bot.add_cog(Graphing(bot))
