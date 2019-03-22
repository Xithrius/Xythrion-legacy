from discord.ext import commands as comms
import discord
import datetime
import urllib.request
import json
import configparser

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
                # Running the bot
                checkToken = False
            except FileNotFoundError:
                token = input('Input discord bot token: ')
                config = configparser.ConfigParser()
                config['weather'] = {'token': token}
                with open(path('credentials', 'config.ini'), 'w') as f:
                    config.write(f)

        with urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?{args[0]}={args[1]},{args[2]}&APPID={token}') as url:
            data = json.loads(url.read().decode())

        with open(path('data_dump', 'weather.json'), 'w') as f:
            json.dump(data, f)

        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=8))
        embed.add_field(name='Location: ', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(WeatherCog(bot))
