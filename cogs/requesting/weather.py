"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import json
from typing import Union

from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from modules import http_get, path


class Weather(comms.Cog):
    """Summary for Weather

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.cooldown(1, 1, BucketType.user)
    @comms.command()
    async def weather(self, ctx, area: Union[str, int], country: str = 'US'):
        """Getting Weather for a planet or for a zip code on Earth.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            area (:obj:`typing.Union[str, int]`): Either the zip code on Earth, just or 'mars'.
            country (str, optional): The country within the US, unless on Mars, this is ignored.

        """
        if isinstance(area, int):
            t = self.bot.config['openweathermap']
            url = f'https://api.openweathermap.org/data/2.5/forecast?zip={country.upper()},{area}&appid={t}'
            info = await http_get(url, session=self.bot.session)

        elif area.lower() == 'mars':
            t = self.bot.config['nasa']
            url = f'https://api.nasa.gov/insight_weather/?api_key={t}&feedtype=json&ver=1.0'
            info = await http_get(url, session=self.bot.session)
            with open(path('tmp', 'mars.json'), 'w') as f:
                json.dump(info, f, indent=3)


def setup(bot):
    bot.add_cog(Weather(bot))


""" Safely pause currently running async function to generate image:

lock = asyncio.Lock()

async with lock:
    func = functools.partial(self.create_table, info)
    f = await self.bot.loop.run_in_executor(None, func)

f = discord.File(path('tmp', f), filename=f)
embed = discord.Embed()
embed.set_image(url=f'attachment://{f}')
await ctx.send(file=f, embed=embed)


Manipulating OpenWeatherMap JSON response:

for I in _json:
    lst[I['dt']] = {
        **{k: v for k, v in I['main'].items() if k in ['temp', 'temp_min', 'temp_max', 'humidity']},
        **I['wind'],
        'description': I['weather'][0]['description']
    }
lst = collections.OrderedDict(sorted(lst.items()))

collections.defaultdict(list)
datetime.datetime.fromtimestamp(k).strftime('%A')
"""
