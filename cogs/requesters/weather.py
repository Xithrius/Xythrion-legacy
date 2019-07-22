"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import platform
import time
import json
import aiohttp
import sqlite3
import os
import asyncio
import datetime

from discord.ext import commands as comms
import discord

from handlers.modules.output import now, path, printc


class Weather_Requester(comms.Cog):
    """ Get information from OpenWeatherMap """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task for checking token
        """
        self.bot = bot
        self.db_path = path('repository', 'database', 'weather.db')

        if not os.path.isfile(self.db_path):
            self.createDB()

        self.load_credentials = self.bot.loop.create_task(self.load_weather())

    def createDB(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE WeatherDB(time INTEGER NOT NULL PRIMARY KEY UNIQUE, high INTEGER, low INTEGER, humidity INTEGER, sunrise INTEGER, sunset INTEGER)''')
        self.conn.commit()
        self.conn.close()

    def weatherData(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        try:
            self.conn.commit()
            c.execute('''SELECT time FROM WeatherDB''')
            checkDate = c.fetchall()[0]
            x = not len(checkDate)
            y = not datetime.datetime.date(now()) == datetime.datetime.date(datetime.datetime.fromtimestamp(checkDate[0]))
            checker = any((x, y))
            if checker:
                c.execute('''INSERT INTO WeatherDB VALUES (?, ?, ?, ?, ?, ?)''', (datetime.datetime.date(now()),))
        except Exception as e:
            print(e)

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.load_credentials.cancel()

    """ Background tasks """

    async def load_weather(self):
        """ Checks if openweathermap is accessable """
        await self.bot.wait_until_ready()
        self.active_weather = False
        while not self.bot.is_closed():
            self.token = json.load(open(path('handlers', 'configuration', 'config.json')))['weather']
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip=12345,us&APPID={self.token}') as test_response:
                    if test_response.status == 200:
                        if not self.active_weather:
                            printc('[ ! ]: WEATHER SERVICE AVAILABLE')
                        self.active_weather = True
                    else:
                        printc(f'WARNING: WEATHER SERVICE NOT AVAILABLE: {test_response.status}')
            if self.active_weather:
                self.weatherData()
                await asyncio.sleep(60)

    """ Commands """

    @comms.group()
    async def weather(self, ctx):
        """ Helps the user with weather """
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
        """ Using the OpenWeatherMap API to complete requests for weather in a location """
        try:
            await ctx.message.delete()
        except Exception as e:
            pass
        if self.active_weather:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip={args[0]},{args[1]}&APPID={self.token}') as r:
                    if r.status == 200:
                        data = await r.json()
                        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=now())
                        embed.add_field(name='Location:', value=f"{data['name']}, {args[0]}, {data['sys']['country']}", inline=False)
                        embed.add_field(name='Weather Type:', value=data['weather'][0]['description'], inline=False)
                        embed.add_field(name='Temperature:', value=f"Now: {data['main']['temp']} °F\nLow: {data['main']['temp_min']} °F\nHigh: {data['main']['temp_max']} °F", inline=False)
                        embed.add_field(name='Humidity:', value=f"{data['main']['humidity']}%", inline=False)
                        embed.add_field(name='Sunrise:', value=time.ctime(data['sys']['sunrise']), inline=False)
                        embed.add_field(name='Sunset:', value=time.ctime(data['sys']['sunset']), inline=False)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await ctx.author.send(embed=embed)
                    else:
                        await ctx.send(f'Weather: status code {r.status}')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
