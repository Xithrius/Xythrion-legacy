import functools
import os
from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from discord.ext.commands import Cog, Context, group
from tabulate import tabulate

from xythrion.bot import Xythrion
from xythrion.constants import WeatherAPIs
from xythrion.utils import Graph, c2f, check_for_subcommands, http_get, k2c, k2f

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
        if ctx.invoked_subcommand is None:
            await check_for_subcommands(ctx)

    @weather.command()
    async def earth(self, ctx: Context, zip_code: int, country_code: str = 'US') -> None:
        """Getting weather for the planet of Earth."""
        _json = await http_get(
            EARTH_URL.format(zip_code, country_code.upper(), WeatherAPIs.EARTH), session=self.bot.session)

        lst, dates = [], []
        for i in _json['list']:
            lst.append(
                [k2f(i['main']['temp']), k2c(i['main']['temp']), i['main']['humidity'], i['wind']['speed']])
            dates.append(datetime.fromtimestamp(i['dt']).strftime('%a: %H%p').lower().title())

        titles = ['°F', '°C', 'Humidity (%)', 'Wind (m/s)']

        func = functools.partial(self._create_weather_graph_and_table, ctx, lst, titles, dates, 'Time')
        _graph, _table = await self.bot.loop.run_in_executor(None, func)

        _graph.embed.title = '**Weather on Earth.**'

        await ctx.send(file=_graph.embed.file, embed=_graph.embed, content=_table)

        os.remove(_graph.save_path)

    @weather.command()
    async def mars(self, ctx: Context) -> None:
        """Getting weather for the planet of Mars."""
        _json = await http_get(MARS_URL, session=self.bot.session)
        sols = _json['sol_keys']
        lst = []
        titles = ['°F', '°C', 'Pressure (Pa)', 'Wind (m/s)']

        for sol in sols:
            try:
                i = _json[sol]
                c = i['AT']['av']
                lst.append([c2f(c), c, i['PRE']['av'], i['HWS']['av']])

            except KeyError:
                break

        func = functools.partial(self._create_weather_graph_and_table, ctx, lst, titles, sols, 'Sol')
        _graph, _table = await self.bot.loop.run_in_executor(None, func)

        _graph.embed.title = f'**Weather on Mars sols {sols[0]}-{sols[-1]}.**'

        await ctx.send(file=_graph.embed.file, embed=_graph.embed, content=_table)

        os.remove(_graph.save_path)

    def _create_weather_graph_and_table(self, ctx: Context, data_lst: List[List[float]],
                                        titles: List[str], days: List[str], day_title: str
                                        ) -> Tuple[Graph, str]:
        """Manipulating JSON data from weather APIs."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
        axes = [ax1, ax2, ax3, ax4]

        lst = np.array(data_lst)

        lst = [lst[:, i] for i in range(lst.shape[1])]

        for i, (ax, title) in enumerate(zip(axes, titles)):
            ax.plot(lst[i])
            ax.set_title(title)
            ax.set_xticklabels(days, rotation=30)

        return Graph(ctx, fig=fig, ax=axes), self._create_table(days, day_title, titles, data_lst)

    @staticmethod
    def _create_table(days: List[str], day_title: str, titles: List[str], lst: List[str]) -> str:
        """Creates a table from the tabulate module."""
        table = tabulate(
            [[days[i]] + x for i, x in enumerate(lst)], [day_title, *titles],
            tablefmt='simple', showindex=False,
            numalign='left', stralign='right',
            floatfmt='.2f'
        )

        return f'```py\n{table}```'
