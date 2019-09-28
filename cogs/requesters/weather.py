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
import aiofiles

from discord.ext import commands as comms
import discord

from modules.output import path, get_filename, ds, convert_coords


class Weather_Requester(comms.Cog):
    """Fetching weather information from the OpenWeatherMap API"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot
        self.token = self.bot.config.services.weather

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
            await ctx.send(f'Type the command **;help {ctx.command}** for help')

    @weather.command()
    async def daily(self, ctx, location, country='US'):
        """

        Args:
            location: The location, being a zip code or a city.
            country: The country in which code the zip code is in (defaults to US).

        Returns:
            A graph with a high and low temperatures for the days within the amount.

        """
        if len(location) == 5 and all((isinstance(i, int) for i in list(location))):
            location_type = 'zip'
        else:
            location_type = 'q'
        async with self.bot.s.get(f'https://api.openweathermap.org/data/2.5/forecast?{location_type}={location},{country}&appid={self.token}') as r:
            assert r.status == 200
            js = await r.json()
            js = js['list'][:7]
            js = {k: v for k, v in js.items() if k == 'dt'}

    @weather.command()
    async def get_map(self, ctx, postal_code, zoom=5, layer='temp'):
        layer_types = {
            'clouds': 'clouds_new',
            'rain': 'precipitation_new',
            'pressure': 'pressure_new',
            'wind': 'wind_new',
            'temp': 'temp_new'
        }
        if layer not in layer_types.keys():
            await ctx.send(f'Layer options: {", ".join(str(y) for y in layer_types.keys())}')
            return
        lst = convert_coords(postal_code, zoom)
        link = f'https://tile.openweathermap.org/map/{layer_types[layer]}/{zoom}/{lst[0]}/{lst[1]}.png?appid={self.token}'
        async with self.bot.s.get(link) as r:
            assert r.status == 200
            e = discord.Embed(colour=discord.Color.orange())
            e.set_image(url=link)
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
