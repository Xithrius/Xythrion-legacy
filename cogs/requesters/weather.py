"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * Nothing

"""


import matplotlib.pyplot as plt
import numpy as np
import json
import os
import datetime

from discord.ext import commands as comms
import discord

from modules.output import path, get_filename, ds


class Weather_Requester(comms.Cog):
    """Fetching weather information from WeatherBit.io"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """Commands are only passed if the service is available

        Returns:
            True or False depending on the availability of the service

        """
        return self.bot.requester_status['weather']

    """ Commands """

    @comms.group()
    async def weather(self, ctx):
        """The weather group command for commands that are weather related.

        Args:
            ctx: Context object where the command is called.

        Returns:
            The built-in help command if no group command is passed

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @weather.command()
    async def daily(self, ctx, zip_code, amount=7, country='US'):
        """

        Args:
            ctx: Context object where the command is called.
            _zip (int): The zip code of a country.
            amount (int): How many days ahead the graph should be (including today)
            country (str): The country in which code the zip code is in.

        Raises:
            A possible error depending on service availability

        Returns:
            A graph with a high and low temperatures for the days within the amount.

        """
        async with self.bot.s.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={zip_code},{country.upper()}&units=I&key={self.bot.config.services.weather}') as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data'][:amount]
                requests = ['valid_date', 'max_temp', 'min_temp']
                dates = [[v for k, v in _dict.items() if k in requests] for _dict in info]
                highs = [x[1] for x in dates]
                lows = [x[2] for x in dates]
                plt.plot([x[0] for x in dates], highs, linestyle='solid', label="high")
                plt.plot([x[0] for x in dates], lows, linestyle='solid', label="low")
                max_temp, min_temp = max(highs), min(lows)
                plt.xticks(rotation='vertical')
                plt.yticks(ticks=np.arange(min_temp, max_temp + 1, 5))
                plt.legend()
                plt.grid()
                plt.xlabel("Date")
                plt.ylabel("Temperature (°F)")
                plt.title(f"Zip {zip_code}, {country}: High/low temperatures")
                plt.gcf().autofmt_xdate()
                filename = get_filename(ctx.message.author.id, '.png')
                plt.savefig(path('tmp', filename))
                plt.clf()
                await ctx.send(file=discord.File(path('tmp', filename)))
                os.remove(path('tmp', filename))
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
