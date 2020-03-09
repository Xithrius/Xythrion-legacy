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

from modules import gen_filename, kelvin_to_celcius, kelvin_to_fahrenheit, path


class Weather(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

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
            with open(path('tmp', 'tmp.json'), 'w') as f:
                json.dump(lst, f, indent=3)


def setup(bot):
    bot.add_cog(Weather(bot))
