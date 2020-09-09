from datetime import datetime
from typing import List

from discord.ext.commands import Cog, Context, group
from tabulate import tabulate

from xythrion.bot import Xythrion
from xythrion.constants import WeatherAPIs
from xythrion.utils import c2f, c2k, http_get, k2c, k2f


class Weather(Cog, command_attrs=dict(hidden=True, enabled=False)):
    """Weather for Earth and Mars."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @staticmethod
    async def create_table(lst: List[str], titles: List[str]) -> str:
        """Creates a table from the tabulate module."""
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

        return table

    @group()
    async def weather(self, ctx: Context) -> None:
        """Getting Weather for different planets."""
        pass

    @weather.command()
    async def earth(self, ctx: Context, zip_code: int, country_code: str = 'US') -> None:
        """Getting weather for planet Earth."""
        c = country_code.upper()
        url = f'https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{c}&appid={WeatherAPIs.EARTH}'
        _json = await http_get(url, session=self.bot.session)

        lst = {}
        for i in _json['list']:
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
        table = await self.create_table(lst, titles)

        await ctx.send(f'```\n{table}```')

    @weather.command()
    async def mars(self, ctx: Context) -> None:
        """Getting weather for planet Mars."""
        url = f'https://api.nasa.gov/insight_weather/?api_key={WeatherAPIs.MARS}&feedtype=json&ver=1.0'
        _json = await http_get(url, session=self.bot.session)

        sol_keys = _json['sol_keys']
        lst = {}
        titles = ['Sol', '°K', '°F', '°C', 'Pressure (Pa)', 'Wind (m/s)']

        for sol in sol_keys:
            i = _json[sol]
            c = i['AT']['av']
            lst[sol] = [
                c2k(c), c2f(c), c,
                i['PRE']['av'],
                i['HWS']['av']
            ]

        lst = [[sol_keys[i]] + v for i, v in enumerate(lst.values())]
        table = await self.create_table(lst, titles)

        await ctx.send(f'```\n{table}```')
