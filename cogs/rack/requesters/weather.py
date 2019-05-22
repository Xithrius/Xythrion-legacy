'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform
import time
import pytemperature
import requests
import json

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# OpenWeatherMap.org request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from OpenWeatherMap
# //////////////////////////////////////////////////////////////////////////// #


class Weather_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.command(name='weather')
    async def get_weather(self, ctx, *args):
        """
        Using the OpenWeatherMap API to complete requests for weather in a location
        """
        checkToken = True
        while checkToken:
            try:
                token = json.load(open(path('JAiRU', 'configuration', 'config.json')))['weather']
                checkToken = False
            except FileNotFoundError:
                print('WARNING: OPENWEATHERMAP TOKEN NOT FOUND')
        data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?{args[0]}={args[1]},{args[2]}&APPID={token}').json()
        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=now())
        embed.add_field(name='Location:', value=f"{data['name']}, {args[1]}, {data['sys']['country']}", inline=False)
        embed.add_field(name='Weather Type:', value=data['weather'][0]['description'], inline=False)
        embed.add_field(name='Temperature:', value=f"Now: {pytemperature.k2f(data['main']['temp'])} °F\nLow: {pytemperature.k2f(data['main']['temp_min'])} °F\nHigh: {pytemperature.k2f(data['main']['temp_max'])} °F", inline=False)
        embed.add_field(name='Humidity:', value=f"{data['main']['humidity']}%", inline=False)
        embed.add_field(name='Visibility', value=f"{data['visibility']} meters", inline=False)
        embed.add_field(name='Sunrise:', value=time.ctime(data['sys']['sunrise']), inline=False)
        embed.add_field(name='Sunset:', value=time.ctime(data['sys']['sunset']), inline=False)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
