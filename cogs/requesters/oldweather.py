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
import sys

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
                async with session.get(f'http://api.openweathermap.org/data/2.5/weather?zip={args[0]},{args[1]}&APPID={self.bot.tokens["weather"]}') as r:
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

    async def cog_check(self, ctx):
        return self.bot.services[os.path.basename(__file__)[:-3]]

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def init_weather(self, ctx):
        c = self.conn.cursor()


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
