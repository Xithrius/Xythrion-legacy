"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3
import asyncio
import datetime

from discord.ext import commands as comms
import discord

from handlers.modules.output import now, path, get_aiohttp, printc


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

        # self.background_weather = self.bot.loop.create_task(self.collect_weather())

    def createDB(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE WeatherDB (id INTEGER,
                                            time INTEGER,
                                            high INTEGER,
                                            low INTEGER,
                                            humidity INTEGER,
                                            sunrise INTEGER,
                                            sunset INTEGER)''')
        self.conn.commit()
        self.conn.close()

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.message.author.id in self.bot.services[os.path.basename(__file__)[:-3]]

    def cog_unload(self):
        """ """
        try:
            self.conn.close()
        except Exception as e:
            pass

    async def collect_weather(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.conn = sqlite3.connect(path('repository', 'database', 'user_requests.db'))
            c = self.conn.cursor()
            c.execute('''SELECT id, weather FROM RequestsDB''')
            requests = c.fetchall()
            self.conn.close()
            self.conn = sqlite3.connect(self.db_path)
            c = self.conn.cursor()
            c.execute('''SELECT id, time from WeatherDB''')
            weatherDB = c.fetchall()
            if len(requests):
                for request in requests:
                    _id = request[0]
                    try:
                        r = [x[0] for x in weatherDB].index(_id)
                        lastRequest = weatherDB[r]
                        today = datetime.datetime.date(now())
                        lastDate = datetime.datetime.date(datetime.datetime.fromtimestamp(lastRequest[1]))
                        if today != lastDate:
                            raise ValueError
                    except ValueError:
                        pass
            self.conn.close()
            await asyncio.sleep(60)
            """
            for request in info:
                rn = datetime.datetime.date(now())
                anotherDate = datetime.datetime.date(datetime.datetime.fromtimestamp(weatherInfo[0][1]))
                print(rn, anotherDate)
                if all((rn != anotherDate), (weatherInfo[0][0] in info)):
                    _id = request[0]
                    reqInfo = await get_aiohttp(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={request[1]},{request[2]}&units=I&key={self.bot.tokens["weather"]}')
                    reqInfo = reqInfo['data'][0]
                    requests = ['ts', 'max_temp', 'min_temp', 'rh', 'sunrise_ts', 'sunset_ts']
                    reqInfo = {k: v for k, v in reqInfo.items() if k in requests}
                    reqInfo = tuple([_id] + [x[1] for x in sorted(reqInfo.items(), key=lambda pair: requests.index(pair[0]))])
                    printc(reqInfo)
                    c.execute('''INSERT INTO WeatherDB VALUES (?, ?, ?, ?, ?, ?, ?)''', reqInfo)
                    self.conn.commit()
            """

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def init_weather(self, ctx, zip_code, country='US'):
        self.conn = sqlite3.connect(path('repository', 'database', 'user_requests.db'))
        c = self.conn.cursor()
        c.execute('''INSERT INTO RequestsDB (id, weather) VALUES (?, ?)''', (ctx.message.author.id, f'{zip_code},{country.upper()}'))
        self.conn.commit()
        await ctx.send(f'Weather collection requester **enabled** for {zip_code}, {country.upper()}')

    @comms.command()
    async def daily(self, ctx, zip_code, amount=7, country='US'):
        info = await get_aiohttp(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={zip_code},{country.upper()}&units=I&key={self.bot.tokens["weather"]}')
        info = info['data'][:amount]
        requests = ['valid_date', 'max_temp', 'min_temp']
        dates = [[v for k, v in dict.items() if k in requests] for dict in info]
        highs = [x[1] for x in dates]
        lows = [x[2] for x in dates]
        plt.plot([x[0] for x in dates], highs, linestyle='dotted', label="high")
        plt.plot([x[0] for x in dates], lows, linestyle='dotted', label="low")
        max_temp, min_temp = max(highs + lows), min(highs + lows)
        plt.xticks(rotation='vertical')
        plt.yticks(np.arange(min_temp, max_temp + 1, 5), highs + lows)
        plt.legend()
        plt.grid()
        plt.xlabel("Date")
        plt.ylabel("Temperature (°F)")
        plt.title(f"Zip {zip_code}, {country}: High/low temperatures")
        plt.gcf().autofmt_xdate()
        plt.savefig(path('repository', 'graphs', 'weather.png'))
        plt.clf()
        await ctx.send(file=discord.File(path('repository', 'graphs', 'weather.png')))
        os.remove(path('repository', 'graphs', 'weather.png'))


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
