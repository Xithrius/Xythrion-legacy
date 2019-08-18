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

from handlers.modules.output import now, path, ds, get_filename


class Weather_Requester(comms.Cog):
    """ Get information from WeatherBit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]
        # self.background_weather = self.bot.loop.create_task(self.collect_weather())

    """ Cog events """

    def cog_unload(self):
        # self.background_weather.cancel()
        try:
            self.c.close()
        except Exception:
            pass

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        # return all((ctx.message.author.id in self.bot.owner_ids, self.h))
        return True

    """ Background tasks """

    async def collect_weather(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.c = sqlite3.connect(self.bot.db_path)
            c = self.c.cursor()
            c.execute('''SELECT id, weather FROM Requests''')
            requests = c.fetchall()
            if len(requests):
                for request in requests:  # request = (id, 'zip,country')
                    c.execute('''SELECT id, time FROM Weather WHERE id = ?''', (request[0],))
                    weather_requests = c.fetchall()
                    area = request[1].split(',')
                    if not len(weather_requests):
                        await self.get_weather(request[0], area[0], area[1])
                    else:
                        n = datetime.datetime.date(now())
                        other_date = datetime.datetime.fromtimestamp(weather_requests[0][1])
                        other_date = datetime.datetime.date(other_date)
                        if n > other_date:
                            await self.get_weather(request[0], area[0], area[1])
            await asyncio.sleep(60)

    async def get_weather(self, _id, zip_code, country):
        async with self.bot.s.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={zip_code},{country.upper()}&units=I&key={self.bot.config.services.weather}') as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data'][0]
                c = self.c.cursor()
                c.execute('''INSERT INTO Weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    _id,
                    int(datetime.datetime.timestamp(now())),
                    info['max_temp'],
                    info['min_temp'],
                    info['rh'],
                    info['sunrise_ts'],
                    info['sunset_ts'],
                    info['moonrise_ts'],
                    info['moonset_ts'],
                    info['pop'],
                    info['precip'],
                    info['snow'],
                    info['snow_depth']
                ))
        self.c.commit()

    """ Commands """

    @comms.group()
    async def weather(self, ctx):
        """ """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @weather.command(name='init')
    async def _init(self, ctx, _zip, country='US'):
        """ """
        self.c = sqlite3.connect(self.bot.db_path)
        c = self.c.cursor()
        c.execute('''SELECT id, weather FROM Requests WHERE id = ?''', (ctx.message.author.id,))
        requests = c.fetchall()
        if not len(requests):
            c.execute('''INSERT INTO Requests (id, weather) VALUES (?, ?)''', (ctx.message.author.id, f'{_zip},{country}'))
            self.c.commit()
        else:
            await ctx.send('You have already requested an area! Notify owner to request a change to your area.')
        self.c.close()

    @weather.command()
    async def daily(self, ctx, zip_code, amount=7, country='US'):
        """ """
        async with self.bot.s.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={zip_code},{country.upper()}&units=I&key={self.bot.config.services.weather}') as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data'][:amount]
                requests = ['valid_date', 'max_temp', 'min_temp']
                dates = [[v for k, v in _dict.items() if k in requests] for _dict in info]
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
                filename = get_filename(ctx.message.author.id, '.png')
                plt.savefig(path('repository', 'tmp', filename))
                plt.clf()
                await ctx.send(file=discord.File(path('repository', 'tmp', filename)))
                os.remove(path('repository', 'tmp', filename))
            else:
                await ctx.send(f'Requester failed. Status code: **{r.status}**')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
