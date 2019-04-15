'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import json
import time
import datetime
import platform
import urllib
import configparser

from discord.ext import commands as comms
import discord
import pytemperature

from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Weather cog
# /////////////////////////////////////////////////////////
# Get weather for a location
# //////////////////////////////////////////////////////////////////////////// #


class WeatherCog(comms.Cog):

    # //////////////////////// # Object(s): bot
    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Get weather for an input location
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
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(WeatherCog(bot))
