from discord.ext import commands as comms
import discord
import datetime
# from lxml import html
# import requests


class WeatherCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='weather')
    async def get_weather(self, ctx):
        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=8))
        embed.add_field(name='Location: ', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command()
    async def test(self, ctx, *, args):
        await ctx.send(args)

# http://api.openweathermap.org/data/2.5/weather?zip=&APPID=


def setup(bot):
    bot.add_cog(WeatherCog(bot))


'''
@comms.command()
async def etg(self, ctx, *, args):
    if objectType in ['gungeoneer', 'gun', 'item', 'boss', 'cotg']:
        if objectType == 'gungeoneer':
            page = requests.get('https://enterthegungeon.gamepedia.com/Gungeoneers')
            tree = html.fromstring(page.content)
            titles = tree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[1]/th[1]/text()')
        elif objectType == 'gun':
            page = requests.get('https://enterthegungeon.gamepedia.com/Guns')
            tree = html.fromstring(page.content)
'''
