"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    @comms.cooldown(1, 1, BucketType.default)
    @comms.command()
    async def weather(self, ctx, option, _zip: int, country_code='US'):
        option, options, country_code = option.lower(), ['forecast', 'weather'], country_code.upper()
        if option.lower() not in ['forecast', 'weather']:
            return await ctx.send(f'Selected option for request is not in {", ".join(str(y) for y in options)}')
        url = f'https://api.openweathermap.org/data/2.5/{option}?zip={_zip},{country_code}&appid={self.bot.config["weather"]}'
        async with self.bot.session.get(url, loop=self.bot.loop):
            assert r.status == 200
            js = await r.json()


def setup(bot):
    bot.add_cog(Weather(bot))