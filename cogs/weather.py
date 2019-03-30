#!/usr/bin/env python


'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import datetime
import configparser
import urllib.request
import json
import time
import platform

import discord
from discord.ext import commands as comms
import pytemperature

from essentials.pathing import path  # , mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


class WeatherCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='weather')
    async def get_weather(self, ctx, *args):
        checkToken = True
        while checkToken:
            try:
                config = configparser.ConfigParser()
                config.read(path('credentials', 'config.ini'))
                token = config['weather']['token']
                checkToken = False
            except FileNotFoundError:
                token = input('Input weather API token: ')
                config = configparser.ConfigParser()
                config['weather'] = {'token': token}
                with open(path('credentials', 'config.ini'), 'w') as f:
                    config.write(f)

        with urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?{args[0]}={args[1]},{args[2]}&APPID={token}') as url:
            data = json.loads(url.read().decode())

        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))

        embed.add_field(name='Location:', value=f"{data['name']}, {args[1]}, {data['sys']['country']}", inline=False)
        embed.add_field(name='Weather Type:', value=data['weather'][0]['description'], inline=False)
        embed.add_field(name='Temperature:', value=f"Now: {pytemperature.k2f(data['main']['temp'])} °F\nLow: {pytemperature.k2f(data['main']['temp_min'])} °F\nHigh: {pytemperature.k2f(data['main']['temp_max'])} °F", inline=False)
        embed.add_field(name='Humidity:', value=f"{data['main']['humidity']}%", inline=False)
        embed.add_field(name='Visibility', value=f"{data['visibility']} meters", inline=False)
        embed.add_field(name='Sunrise:', value=time.ctime(data['sys']['sunrise']), inline=False)
        embed.add_field(name='Sunset:', value=time.ctime(data['sys']['sunset']), inline=False)

        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(WeatherCog(bot))
