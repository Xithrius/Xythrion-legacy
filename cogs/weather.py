from discord.ext import commands as comms
import discord
import datetime
import urllib.request
import json
import configparser
import pytemperature
import time
import platform

from essentials.pathing import path


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
