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

    async def weatherData(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        self.conn.commit()
        c.execute('''SELECT time FROM WeatherDB''')
        # print(datetime.datetime.date(now()))
        # datetime.datetime.date(datetime.datetime.fromtimestamp(checkDate[0]))
        info = c.fetchall()
        if len(info):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip={args[0]},{args[1]}&APPID={self.bot.config["weather"]}') as r:
                    if r.status == 200:
                        data = await r.json()
                        temp = data['main']['temp']
                        low = data['main']['temp_min']
                        high = data['main']['temp_max']
                        hum = data['main']['humidity']
                        sunrise = data['sys']['sunrise']  # time.ctime(sunrise)
                        sunset = data['sys']['sunset']
            c.execute('''INSERT INTO WeatherDB VALUES (?, ?, ?, ?, ?, ?)''', (datetime.datetime.date(now()),
                                                                              temp,
                                                                              low,
                                                                              high,
                                                                              hum,
                                                                              sunrise,
                                                                              sunset))
            self.conn.commit()

    def cog_unload(self):
        """ Cancel background task(s) when cog is unloaded """
        self.load_credentials.cancel()

    """ Background tasks """

    async def load_weather(self):
        """ Checks if openweathermap is accessable """
        await self.bot.wait_until_ready()
        self.active_weather = False
        while not self.bot.is_closed():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip=12345,us&APPID={self.bot.config["weather"]}') as test_response:
                    if test_response.status == 200:
                        if not self.active_weather:
                            printc('[ ! ]: WEATHER SERVICE AVAILABLE')
                        self.active_weather = True
                    else:
                        printc(f'WARNING: WEATHER SERVICE NOT AVAILABLE: {test_response.status}')
            if self.active_weather:
                await self.weatherData()
                await asyncio.sleep(60)

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def init_weather(self, ctx):
        c = self.conn.cursor()


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
