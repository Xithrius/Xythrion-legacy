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
import asyncio

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path
from rehasher.containers.output.printer import printc


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
        self.load_credentials = self.bot.loop.create_task(self.load_weather())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_credentials.cancel()

    """

    Background tasks

    """
    async def load_weather(self):
        """
        Checks if openweathermap is accessable
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.active_weather = False
                if not self.active_weather:
                printc('[...]: CHECKING WEATHER SCRIPT TOKEN')
                f = json.load(open(path('rehasher', 'configuration', 'config.json')))['weather']
                requests.get(f'http://api.openweathermap.org/data/2.5/weather?zip=12345,us&APPID={f['token']}').json()
                if response in []:
                    raise ValueError(f'WARNING: WEATHER REQUESTS CANNOT BE ACTIVATED {response}')
                    self.active_weather = False
                    asyncio.sleep(60)
                else:
                    self.active_weather = True
                    printc('[ ! ]: WEATHER SCRIPT TOKEN ACTIVATED')

    """

    Commands

    """
    @comms.group(name='weather')
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

    @get_weather.command(name='help')
    async def weather_help(self, ctx):
        """
        Helps the user with weather
        """
        embed = discord.Embed(title=':thunder_cloud_rain: `Usage of the weather command` :thunder_cloud_rain:', colour=0xc27c0e, timestamp=now())
        help = '''`$weather zip <zip> <country abbreviation>`
                  `<zip>`: `Zip code (postal address)`
                  `<country abbreviation>`: `abbreviation used for the country which the zip code resides in`'''
        embed.add_field(name='Usage:', value=help)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
