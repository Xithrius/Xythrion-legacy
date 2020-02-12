"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import discord
from discord.ext import commands as comms


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        """ """
        self.bot = bot

    @comms.command(enabled=False)
    async def weather(self, ctx, zip: int):
        """ """
        url = ''
        async with self.bot.session.get(url) as r:
            assert r.status == 200
            js = await r.json()
            # NOTE: Do stuff


def setup(bot):
    bot.add_cog(Weather(bot))
