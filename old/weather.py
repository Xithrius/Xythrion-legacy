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
import sqlite3
import asyncio
import datetime

from discord.ext import commands as comms
import discord

from modules.output import now, path, ds, get_filename


class Weather_Requester(comms.Cog):
    """Fetching weather information from WeatherBit.io"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

        if not os.path.isfile(self.db_path):

            #: Building file and connecting to the empty database file
            self.c = sqlite3.connect(self.db_path)
            c = self.c.cursor()

            c.execute('''CREATE TABLE Weather (id INTEGER,
                                        time INTEGER,
                                        high INTEGER,
                                        low INTEGER,
                                        humidity INTEGER,
                                        sunrise INTEGER,
                                        sunset INTEGER,
                                        moonrise INTEGER,
                                        moonset INTEGER,
                                        pop INTEGER,
                                        precip INTEGER,
                                        snow INTEGER,
                                        snow_depth INTEGER)''')

            #: Closing database for now
            self.c.commit()
            self.c.close()

        #: Creating attribute of weather availability
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]

        #: Creation of background task for collecting weather initiated by requests of users
        self.background_weather = self.bot.loop.create_task(self.collect_weather())

    """ Cog events """

    def cog_unload(self):
        """Safely cancels background tasks and possible database connection.

        Raises:
            A very rare error when canceling the background task

        Returns:
            Hopefully nothing unless an error occurs

        """
        self.background_weather.cancel()
        try:
            self.c.close()
        except Exception:
            pass

    """ Permission checking """

    async def cog_check(self, ctx):
        """Commands are only passed if the service is available

        Returns:
            True or False depending on the availability of the service

        """
        return self.h

    """ Background tasks """

    async def collect_weather(self):
        """Collects weather for a user's requested singular zip code once a day.

        Returns:
            Data from weatherbit.io into the requests.db's Weather table.

        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.c = sqlite3.connect(self.bot.db_path)
            c = self.c.cursor()
            c.execute('''SELECT id, weather FROM Requests''')
            requests = c.fetchall()
            if len(requests):
                for request in requests:  # request = (id, 'zip,country')
                    c.execute(
                        '''SELECT id, time FROM Weather WHERE id = ?''', (request[0],))
                    weather_requests = c.fetchall()
                    area = request[1].split(',')
                    if not len(weather_requests):
                        await self.get_weather(request[0], area[0], area[1])
                    else:
                        n = datetime.datetime.date(now())
                        other_date = datetime.datetime.fromtimestamp(
                            weather_requests[-1][1])
                        other_date = datetime.datetime.date(other_date)
                        if n > other_date:
                            await self.get_weather(request[0], area[0], area[1])
            await asyncio.sleep(60)

    async def get_weather(self, _id, zip_code, country):
        """Inserting weather into the database.

        Args:
            _id (int): The unique ID of a user.
            zip_code (int): Requested zip code from a user.
            country (str): The country the zip_code is within.

        Raises:
            Possible fatal error when requesting from the service.

        Returns:
            A large amount of data that is promptly inserted in the database of weather requests.

        """
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
        """The weather group command for commands that are weather related.

        Args:
            ctx: Context object where the command is called.

        Returns:
            The built-in help command if no group command is passed

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **.help {ctx.command}** for help')

    @weather.command(name='init')
    async def _init(self, ctx, _zip, country='US'):
        """Initiates the daily requesting for a user and their zip code

        Args:
            ctx: Context object where the command is called.
            _zip (int): The zip code of a country.
            country (str): The country in which code the zip code is in.

        Raises:
            An error if the user already has a request running

        Returns:
            A success message, or a fatal error depending on if the user has a request running or not.

        """
        self.c = sqlite3.connect(self.bot.db_path)
        c = self.c.cursor()
        c.execute('''SELECT id, weather FROM Requests WHERE id = ?''',
                  (ctx.message.author.id,))
        requests = c.fetchall()
        if not len(requests):
            c.execute('''INSERT INTO Requests (id, weather) VALUES (?, ?)''',
                      (ctx.message.author.id, f'{_zip},{country}'))
            self.c.commit()
            await ctx.send('Weather requester initiated.')
        else:
            await ctx.send('You have already requested an area! Notify owner to request a change to your area.')
        self.c.close()

    @weather.command()
    async def daily(self, ctx, zip_code, amount=7, country='US'):
        """

        Args:
            ctx: Context object where the command is called.
            _zip (int): The zip code of a country.
            amount (int): How many days ahead the graph should be (including today)
            country (str): The country in which code the zip code is in.

        Raises:
            A possible error depending on service availability

        Returns:
            A graph with a high and low temperatures for the days within the amount.

        """
        async with self.bot.s.get(f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={zip_code},{country.upper()}&units=I&key={self.bot.config.services.weather}') as r:
            if r.status == 200:
                _json = await r.json()
                info = _json['data'][:amount]
                requests = ['valid_date', 'max_temp', 'min_temp']

                dates = [[v for k, v in _dict.items() if k in requests] for _dict in info]
                highs = [x[1] for x in dates]
                lows = [x[2] for x in dates]
                plt.plot([x[0] for x in dates], highs, linestyle='solid', label="high")
                plt.plot([x[0] for x in dates], lows, linestyle='solid', label="low")
                max_temp, min_temp = max(highs), min(lows)
                plt.xticks(rotation='vertical')
                plt.yticks(ticks=np.arange(min_temp, max_temp + 1, 5))

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

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Catches errors specifically within this cog

        Args:
            ctx: Context object where the command is called.
            error: Error object of what the command caused.

        Returns:
            A specific string depending on the error within the cog.

        """
        if ctx.command.cog_name == self.__class__.__name__:
            await ctx.send('Requester failed to get subreddit information.')


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
