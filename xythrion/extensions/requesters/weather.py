import os

import matplotlib.pyplot as plt
import numpy as np
from discord.ext.commands import Cog, Context, group

from xythrion.bot import Xythrion
from xythrion.constants import WeatherAPIs
from xythrion.utils import Graph, c2f, http_get

EARTH_URL = 'https://api.openweathermap.org/data/2.5/forecast?zip={0},{1}&appid={2}'
MARS_URL = f'https://api.nasa.gov/insight_weather/?api_key={WeatherAPIs.MARS}&feedtype=json&ver=1.0'


class Weather(Cog):
    """Weather for different planets."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checks if the user and/or guild has permissions for this command."""
        return await self.bot.database.check_if_blocked(ctx)

    @group()
    async def weather(self, ctx: Context) -> None:
        """Getting Weather for different planets."""
        pass

    # @weather.command()
    # async def earth(self, ctx: Context, zip_code: int, country_code: str = 'US') -> None:
    #     """Getting weather for planet Earth."""
    #     _json = await http_get(
    #         EARTH_URL.format(zip_code, country_code.upper(), WeatherAPIs.EARTH), session=self.bot.session)
    #
    #     lst = {}
    #     for i in _json['list']:
    #         lst[i['dt']] = {
    #             'description': i['weather'][0]['description'],
    #             '°K': i['main']['temp'], '°F': k2f(i['main']['temp']), '°C': k2c(i['main']['temp']),
    #             'humidity': i['main']['humidity'],
    #             'wind speed': i['wind']['speed']
    #         }
    #
    #     titles = ['Date', 'Description', '°K', '°F', '°C', 'Humidity (%)', 'Wind (m/s)']
    #     dates = [
    #         datetime.fromtimestamp(k).strftime('%A, %I:%M%p').lower().capitalize() for k in lst.keys()
    #     ]
    #     lst = [[dates[i]] + list(v.values()) for i, v in enumerate(lst.values())]
    #     table = await self.create_table(lst, titles)
    #
    #     await ctx.send(f'```\n{table}```')

    @staticmethod
    def create_mars_graph(ctx: Context, _json: dict) -> Graph:
        """Manipulating JSON data from the NASA Mars API."""
        sols = _json['sol_keys']
        lst = []
        titles = ['°F', '°C', 'Pressure (Pa)', 'Wind (m/s)']

        for sol in sols:
            i = _json[sol]
            c = i['AT']['av']
            lst.append([c2f(c), c, i['PRE']['av'], i['HWS']['av']])

        fig, axes = plt.subplots(nrows=2, ncols=2)

        lst = np.array(lst)
        lst = [lst[:, i] for i in range(lst.shape[1])]

        for i, (ax, title) in enumerate(zip(sum(axes, []), titles)):
            ax.plot(lst[i])
            ax.title(label=title)
            ax.set_xticklabels(sols)

        return Graph(ctx, fig=fig)

    @weather.command()
    async def mars(self, ctx: Context) -> None:
        """Getting weather for planet Mars."""
        _json = await http_get(MARS_URL, session=self.bot.session)
        _graph = self.bot.loop.run_in_executor(None, self.create_mars_graph, ctx, _json)

        await ctx.send(file=_graph.embed.file, embed=_graph.embed)

        os.remove(_graph.save_path)

    # @staticmethod
    # async def create_table(lst: List[str], titles: List[str]) -> str:
    #     """Creates a table from the tabulate module."""
    #     table = tabulate(
    #         lst, titles,
    #         tablefmt='simple', showindex=False,
    #         numalign='left', stralign='right',
    #         floatfmt='.2f'
    #     ).split('\n')
    #
    #
    #     return table
