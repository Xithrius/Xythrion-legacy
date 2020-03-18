"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import collections

from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from matplotlib import pyplot as plt


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    @comms.cooldown(1, 1, BucketType.user)
    @comms.group()
    async def weather(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed.')

        """Takes zip code and graph options and returns a plot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            zip_code (int): The zip code for the weather.
            option (typing.Optional[str]): Farenheight or Celcius abbreviations.
            country_code (str): The code of a country.

        """

    @weather.command()
    async def earth(self, ctx, zip_code: int, country_code: str = 'US'):
        country_code = country_code.upper()
        url = f'https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={self.bot.config["openweathermap"]}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status
            _json = await r.json()
            _json = _json['list']

        plt.clf()
        lst = {}

        for I in _json:
            lst[I['dt']] = {
                **{k: v for k, v in I['main'].items() if k in ['temp', 'temp_min', 'temp_max', 'humidity']},
                **I['wind'],
                'description': I['weather'][0]['description']
            }
        lst = collections.OrderedDict(sorted(lst.items()))

        # collections.defaultdict(list)
        # datetime.datetime.fromtimestamp(k).strftime('%A')

    @weather.command()
    async def mars(self, ctx):
        url = f'https://api.nasa.gov/insight_weather/?api_key={self.bot.config["nasa"]}&feedtype=json&ver=1.0'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status


def setup(bot):
    bot.add_cog(Weather(bot))
