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
import numpy as np

from modules import gen_filename, kelvin_to_celcius, kelvin_to_fahrenheit as k2f, path


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    def create_plot(self, _json, zip_code, country_code) -> str:
        plt.clf()
        lst = {}

        for I in _json:
            lst[I['dt']] = {
                **{k:v for k, v in I['main'].items() if k in ['temp', 'temp_min', 'temp_max', 'humidity']},
                **I['wind'],
                'description': I['weather'][0]['description']
            }
        lst = collections.OrderedDict(sorted(lst.items()))
        total_days = [datetime.datetime.fromtimestamp(k).strftime('%A').capitalize() for k in lst.keys()]
        
        d = collections.defaultdict(list)
        for k, v in lst.items():
            day = datetime.datetime.fromtimestamp(k).strftime('%A')
            values = [k2f(x) if i in range(0, 3) else x for i, x in enumerate(v.values())]
            if day not in d.keys():
                d[day] = [values]
            else:
                d[day].append(values)

        # Getting the average of all items
        for k, v in d.items():
            length = len(v)
            
            # Summing up all the columns
            arr = np.array([x[:-2] for x in v])
            lst = [round(np.sum(arr[:, i]) / length, 1) for i in range(arr.shape[1])]

            # Adding the most common desc and the sums list together
            # desc = collections.Counter([x[-1] for x in v]).most_common(1)[0][0]
            # lst.append(desc)
            
            # Overwriting in the dictionary
            d[k] = lst

        labels = list(d.keys())
        values = np.array(list(d.values()))

        width = 0.6
        x = np.arange(len(labels))
        # values = np.arange(np.min([v for v in d.values()]), np.max([v for v in d.values()]), 15)
        columns = ['avg temp (°F)', 'low temp (°F)', 'high temp (°F)', 'humidity (%)', 'wind speed (mph)']
        fig, ax = plt.subplots()
        rects = []
        # reacts.append(ax.bar(x + w[0], d.values()[:, 0], w[0], label=labels[0]))
        for i in range(4):
            rects.append(ax.bar(x + (width * (-1 ** i)) / 2, values[:, i], width, label=labels[i]))
        
        for rect in rects:
            break
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        fig.subplots_adjust(left=0.2, bottom=0.2)
        plt.xlabel('Day')
        plt.suptitle('Forecast Information')
        plt.title(f'{zip_code}, {country_code}')
        plt.legend()

        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
        
        return f
        # NOTE: before - https://github.com/Xithrius/Xythrion/blob/1df02a1199f90fa364309e4c07e54d3fe68c1a8c/cogs/requesters/weather.py

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
            _json = await r.json()
            _json = _json['list']
            
        lock = asyncio.Lock()
        async with lock:
            func = functools.partial(self.create_plot, _json, zip_code, country_code)
            f = await self.bot.loop.run_in_executor(None, func)
            # File object for graph
            file = discord.File(path('tmp', f), filename=f)

        await ctx.send(file=file)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Weather(bot))
