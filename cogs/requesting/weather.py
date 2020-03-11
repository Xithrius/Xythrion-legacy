"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools
import os
import typing
import datetime
import json
import collections
import asyncio

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import matplotlib.pyplot as plt

from modules import gen_filename, kelvin_to_celcius, kelvin_to_fahrenheit, path


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    def create_plot(self, lst, zip_code, country_code) -> str:
        plt.clf()

        data = [(datetime.datetime.fromtimestamp(k).strftime('%A'), v['temp']) for k, v in lst.items()]

        # NOTE: TABLE - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.table.html#matplotlib.pyplot.table
        # NOTE: PIE - https://matplotlib.org/api/_as_gen/matplotlib.pyplot.pie.html#matplotlib.pyplot.pie
        # NOTE: before - https://github.com/Xithrius/Xythrion/blob/1df02a1199f90fa364309e4c07e54d3fe68c1a8c/cogs/requesters/weather.py
        plt.hist2d([x[0] for x in data], [kelvin_to_fahrenheit(x[1]) for x in data])
        # plt.grid()
        plt.xlabel('Day')
        plt.ylabel('Temperature (°F)')
        plt.suptitle('Forecast Information')
        plt.title(f'{zip_code}, {country_code}')
        plt.gcf().autofmt_xdate()


        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
        
        return f

    @comms.cooldown(1, 10, BucketType.user)
    @comms.command()
    async def weather(self, ctx, zip_code: int, option: typing.Optional[str] = 'F', *, country_code='US'):
        """Takes zip code and graph options and returns a plot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            zip_code (int): The zip code for the weather.
            amount (int): Optional argument for days, default to 7.
            country_code (str): The code of a country

        """
        country_code = country_code.upper()
        url = f'https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={self.bot.config["weather"]}'
        async with self.bot.session.get(url) as r:
            assert r.status == 200, r.status
            js = await r.json()
        info = js['list']
        lst = {}

        for I in info:
            lst[I['dt']] = {
                **{k:v for k, v in I['main'].items() if k in ['temp', 'temp_min', 'temp_max', 'humidity']},
                'weather': I['weather'][0]['description'],
                **I['wind']
            }
        lst = collections.OrderedDict(sorted(lst.items()))
        
        lock = asyncio.Lock()
        
        async with lock:
            func = functools.partial(self.create_plot, lst, zip_code, country_code)
            f = await self.bot.loop.run_in_executor(None, func)
            # File object for graph
            file = discord.File(path('tmp', f), filename=f)

        await ctx.send(file=file)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Weather(bot))
