"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import traceback
import typing as t
from datetime import datetime

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from tabulate import tabulate

from modules import (
    gen_block, http_get, path, gen_filename, parallel_executor,
    kelvin_to_celcius as k2c, kelvin_to_fahrenheit as k2f,
    celcius_to_kelvin as c2k, celcius_to_fahrenheit as c2f
)


try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
except Exception as e:
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


class Weather(comms.Cog):
    """Putting weather information on graphs and tables.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific functions """

    @parallel_executor
    def create_plot(self, lst, titles) -> str:
        plt.clf()

        print(lst)
        print()
        print(titles)

        # for item in lst:
        #     x, y = item
        #     plt.plot(x, y)

        f = f'{gen_filename()}.png'
        plt.savefig(path('tmp', f), format='png')

        return f

    """ Commands """

    @comms.cooldown(1, 1, BucketType.default)
    @comms.command()
    async def weather(self, ctx, area: t.Union[str, int], country: str = 'US'):
        """Getting Weather for a planet or for a zip code on Earth.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            area (:obj:`typing.Union[str, int]`): Either the zip code on Earth, just or 'mars'.
            country (str, optional): The country within the US, unless on Mars, this is ignored.

        Command examples:
            >>> [prefix]weather 12345
            >>> [prefix]weather mars

        """
        try:
            area = int(area)
        except ValueError:
            pass

        # Earth
        if isinstance(area, int):
            token = self.bot.config['openweathermap']
            c = country.upper()
            url = f'https://api.openweathermap.org/data/2.5/forecast?zip={area},{c}&appid={token}'
            info = await http_get(url, session=self.bot.session)

            lst = {}
            for i in info['list']:
                lst[i['dt']] = {
                    'description': i['weather'][0]['description'],
                    '°K': i['main']['temp'], '°F': k2f(i['main']['temp']), '°C': k2c(i['main']['temp']),
                    'humidity': i['main']['humidity'],
                    'wind speed': i['wind']['speed']
                }

            titles = ['Date', 'Description', '°K', '°F', '°C', 'Humidity (%)', 'Wind (m/s)']
            dates = [
                datetime.fromtimestamp(k).strftime('%A, %I:%M%p').lower().capitalize() for k in lst.keys()
            ]
            lst = [[dates[i]] + list(v.values()) for i, v in enumerate(lst.values())]

        # Mars
        elif area.lower() == 'mars':
            token = self.bot.config['nasa']
            url = f'https://api.nasa.gov/insight_weather/?api_key={token}&feedtype=json&ver=1.0'
            info = await http_get(url, session=self.bot.session)

            # sol = one day on Mars
            sol_keys = info['sol_keys']
            lst = {}
            titles = ['Sol', '°K', '°F', '°C', 'Pressure (Pa)', 'Wind (m/s)']

            for sol in sol_keys:
                i = info[sol]
                c = i['AT']['av']
                lst[sol] = [
                    c2k(c), c2f(c), c,
                    i['PRE']['av'],
                    i['HWS']['av']
                ]

            lst = [[sol_keys[i]] + v for i, v in enumerate(lst.values())]

        file = await self.create_plot(lst, titles)
        return await ctx.send(file=discord.File(path('tmp', file)))

        table = tabulate(
            lst, titles,
            tablefmt='simple', showindex=False,
            numalign='left', stralign='right',
            floatfmt='.2f'
        ).split('\n')

        # Limiting character count
        for i in range(len(table)):
            if sum([len(x) for x in table[:i]]) < 2000:
                continue
            else:
                table = table[:i - 1]

        await ctx.send(gen_block(table))


def setup(bot):
    bot.add_cog(Weather(bot))
