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
    async def daily(self, ctx, location, amount=7, country='US'):
        """

        Args:
            location: The location, being a zip code or a city.
            amount: How many days ahead the graph should be (including today)
            country: The country in which code the zip code is in (defaults to US).

        Returns:
            A graph with a high and low temperatures for the days within the amount.

        """
        if len(location) == 5 and all((isinstance(i, int) for i in list(location))):
            location_type = 'postal_code'
        else:
            location_type = 'city'
        async with self.bot.s.get() as r:
            if r.status == 200:
                js = await r.json()
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')

    @weather.command()
    async def get_map(self, ctx, layer):
        layer_types = {x: f'{x}_new' for x in ['clouds', 'percipitation', 'pressure', 'wind', 'temperature']}
        if layer not in layer_types.keys():
            await ctx.send('')
            return
        y = 1
        x = 1
        z = 0
        async with self.bot.s.get(f'https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={self.token}'):
            if r.status == 200:
                js = await r.json()
                ds.s(js)
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
