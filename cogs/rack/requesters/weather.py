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
import json
import asyncio
import aiohttp

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
        Background task for checking token
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
        if not self.bot.is_closed():
            self.active_weather = False
            if not self.active_weather:
                printc('[...]: CHECKING WEATHER SERVICE AVAILABILITY')
                self.token = json.load(open(path('rehasher', 'configuration', 'config.json')))['weather']
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip=12345,us&APPID={self.token}') as test_response:
                        if test_response.status == 200:
                            printc('[ ! ]: WEATHER SERVICE AVAILABLE')
                            self.active_weather = True
                        else:
                            raise ValueError(f'WARNING: WEATHER SERVICE NOT AVAILABLE {test_response}')

    """

    Commands

    """
    @comms.group()
    async def weather(self, ctx):
        """
        Helps the user with weather
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=':thunder_cloud_rain: `Usage of the weather command` :thunder_cloud_rain:', colour=0xc27c0e, timestamp=now())
            help = '''
            `$weather zip <zip> <country abbreviation>`
            `<zip>`: `Zip code (postal address)`
            `<country abbreviation>`: `abbreviation used for the country which the zip code resides in`
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    @weather.command(name='zip')
    async def weather_by_zip(self, ctx, *args):
        """
        Using the OpenWeatherMap API to complete requests for weather in a location
        """
        if self.active_weather:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip={args[0]},{args[1]}&APPID={self.token}') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=now())
                        embed.add_field(name='Location:', value=f"{data['name']}, {args[0]}, {data['sys']['country']}", inline=False)
                        embed.add_field(name='Weather Type:', value=data['weather'][0]['description'], inline=False)
                        embed.add_field(name='Temperature:', value=f"Now: {pytemperature.k2f(data['main']['temp'])} °F\nLow: {pytemperature.k2f(data['main']['temp_min'])} °F\nHigh: {pytemperature.k2f(data['main']['temp_max'])} °F", inline=False)
                        embed.add_field(name='Humidity:', value=f"{data['main']['humidity']}%", inline=False)
                        embed.add_field(name='Visibility', value=f"{data['visibility']} meters", inline=False)
                        embed.add_field(name='Sunrise:', value=time.ctime(data['sys']['sunrise']), inline=False)
                        embed.add_field(name='Sunset:', value=time.ctime(data['sys']['sunset']), inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.author.send(embed=embed, delete_after=30)
                    else:
                        await ctx.send(f'Weather: status code {r.status}')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
