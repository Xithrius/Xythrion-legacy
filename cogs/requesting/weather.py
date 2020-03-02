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

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from matplotlib import pyplot as plt

from modules import gen_filename, kelvin_to_celcius, kelvin_to_fahrenheit, path


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    def tmp_graph_creation(self):
        requests = ['valid_date', 'max_temp', 'min_temp']
        dates = [[v for k, v in _dict.items() if k in requests] for _dict in info]
        highs = [x[1] for x in dates]
        lows = [x[2] for x in dates]
        plt.plot([x[0] for x in dates], highs, linestyle='solid', label="high")
        plt.plot([x[0] for x in dates], lows, linestyle='solid', label="low")
        max_temp, min_temp = max(highs), min(lows)
        plt.xticks(rotation='vertical')
        plt.yticks(ticks=np.arange(min_temp, max_temp + 1, 5))

    def create_graph(self, info, zip_code, country_code) -> str:
        """Takes weather information to create a graph saved as an image.

        Args:
            info (list):
            zip_code (int): 
            country_code (int): 

        Returns:
            Path of the image for the graph.

        """

        plt.xlabel("Date")
        plt.ylabel("Temperature (°F)")
        plt.gcf().autofmt_xdate()
        plt.title(f"Weather: {zip_code}, {country_code}")
        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f))
        plt.clf()

        return f

    @comms.cooldown(1, 1, BucketType.default)
    @comms.command()
    async def weather(self, ctx, zip_code: int, country_code: str = 'US'):
        """Takes zip code and graph options and returns a plot.

        Args:
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
            with open(path('tmp.json'), 'w') as f:
                json.dump(lst, f, indent=3)


def setup(bot):
    bot.add_cog(Weather(bot))


"""
            fig = plt.figure(constrained_layout=True)
            area = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
            ax1 = fig.add_subplot(area[0, 0])
            ax2 = fig.add_subplot(area[0, 1])
            ax3 = fig.add_subplot(area[1, 0])
            ax4 = fig.add_subplot(area[1, 1])

            # Continue here:
            # https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py


            # ax1.xlabel("Date")
            # ax1.ylabel("Temperature (°F)")
            # ax1.gcf().autofmt_xdate()
            # fig.title(f"Weather: {zip_code}, {country_code}")

            f = f'{gen_filename()}.png'
            fig.savefig(path('tmp', f))
            fig.clf()
            file = discord.File(path('tmp', f), filename=f)
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{f}')
            await ctx.send(file=file, embed=embed)
            os.remove(path('tmp', f))
"""