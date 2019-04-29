'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import requests
import json
import urllib
import configparser
import pytemperature
import time
import datetime
import platform
import os
import asyncio

from discord.ext import commands as comms
import discord

from containers.essentials.pathing import path, mkdir
from containers.essentials.converter import index_days
from containers.scraping.yahoo_finance import get_stock_summary
from containers.output.printer import printc
from containers.QOL.shortened import now
import relay


# //////////////////////////////////////////////////////////////////////////// #
# Reddit.com request cog
# //////////////////////////////////////////////////////////////////////////// #
# Getting information from reddit
# //////////////////////////////////////////////////////////////////////////// #


class Reddit_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.load_script = self.bot.loop.create_task(self.load_reddit_script())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.load_script.cancel()

    """

    Background tasks

    """
    async def load_reddit_script(self):
        """
        Checks if reddit is accessable
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.reddit_script_active = False
            printc('[...]: CHECKING REDDIT SCRIPT CREDENTIALS')
            f = json.load(open(path('relay', 'configuration', 'reddit_config.json')))
            client_auth = requests.auth.HTTPBasicAuth(f['client_ID'], f['client_secret'])
            post_data = {"grant_type": "password", "username": f['username'], "password": f['password']}
            headers = {"User-Agent": f"Relay.py/{relay.__version__} by {f['username']}"}
            response = (requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)).json()
            reset_time = response['expires_in']
            self.headers = {"Authorization": f"{response['token_type']} {response['access_token']}", "User-Agent": f"Relay.py/{relay.__version__} by {f['username']}"}
            response = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
            if response.json() in [{'message': 'Unauthorized', 'error': 401}, {'error': 'invalid_grant'}]:
                printc('WARNING: REDDIT ACCOUNT CANNOT BE ACTIVATED')
                await asyncio.sleep(60)
            else:
                self.reddit_script_active = True
                printc('[ ✓ ]: REDDIT SCRIPT CREDENTIALS ACTIVATED')
                await asyncio.sleep(reset_time + 1)

    """

    Commands

    """
    @comms.command(name='subreddit_top', hidden=True)
    @comms.is_owner()
    async def request_subreddit_top_posts(self, ctx, subreddit):
        """
        Requesting information for a subreddit user
        """
        if self.reddit_script_active:
            response = (requests.get(f'https://oauth.reddit.com/r/{subreddit}/top/', {"limit": 1}, headers=self.headers)).json()
            # await ctx.send(response)
            print(response)

    @comms.command(name='reddit_user', hidden=True)
    @comms.is_owner()
    async def request_user_information(self, ctx, user):
        """
        Requesting information for a reddit user
        """
        if self.reddit_script_active:
            response = (requests.get(f'https://oauth.reddit.com/user/{user}/about/', headers=self.headers)).json()
            data = response['data']
            embed = discord.Embed(title=f'About reddit user {user}:', colour=0xc27c0e, timestamp=now())
            embed.add_field(name='Link to user profile', value=f'[/u/{user}](https://www.reddit.com/u/{user})')
            embed.set_thumbnail(url=data['icon_img'])
            embed.add_field(name='Karma', value=f"Link Karma: {data['link_karma']}, Comment Karma: {data['comment_karma']}")
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)


# //////////////////////////////////////////////////////////////////////////// #
# OpenWeatherMap.org request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from OpenWeatherMap
# //////////////////////////////////////////////////////////////////////////// #


class Weather_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.command(name='weather')
    async def get_weather(self, ctx, *args):
        """
        Get weather for an input location
        """
        checkToken = True
        while checkToken:
            try:
                config = configparser.ConfigParser()
                config.read(path('relay', 'configuration', 'credentials', 'config.ini'))
                token = config['weather']['token']
                checkToken = False
            except FileNotFoundError:
                token = input('Input weather API token: ')
                config = configparser.ConfigParser()
                config['weather'] = {'token': token}
                with open(path('relay', 'configuration', 'credentials', 'config.ini'), 'w') as f:
                    config.write(f)
        with urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?{args[0]}={args[1]},{args[2]}&APPID={token}') as url:
            data = json.loads(url.read().decode())
        embed = discord.Embed(title='Weather', colour=0xc27c0e, timestamp=now())
        embed.add_field(name='Location:', value=f"{data['name']}, {args[1]}, {data['sys']['country']}", inline=False)
        embed.add_field(name='Weather Type:', value=data['weather'][0]['description'], inline=False)
        embed.add_field(name='Temperature:', value=f"Now: {pytemperature.k2f(data['main']['temp'])} °F\nLow: {pytemperature.k2f(data['main']['temp_min'])} °F\nHigh: {pytemperature.k2f(data['main']['temp_max'])} °F", inline=False)
        embed.add_field(name='Humidity:', value=f"{data['main']['humidity']}%", inline=False)
        embed.add_field(name='Visibility', value=f"{data['visibility']} meters", inline=False)
        embed.add_field(name='Sunrise:', value=time.ctime(data['sys']['sunrise']), inline=False)
        embed.add_field(name='Sunset:', value=time.ctime(data['sys']['sunset']), inline=False)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.author.send(embed=embed)


# //////////////////////////////////////////////////////////////////////////// #
# Stock cog
# //////////////////////////////////////////////////////////////////////////// #
# Web scraping the internet for stock information
# //////////////////////////////////////////////////////////////////////////// #


class Stock_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Background task
        """
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_stock_reminders())

    def cog_unload(self):
        """
        Cancel background task(s) when cog is unloaded
        """
        self.bg_task.cancel()

    """

    Commands

    """
    @comms.command(name='stocks')
    async def get_current_stocks(self, ctx, abbreviation, option='low'):
        """ Get information about inputted stock """
        stock_dict = get_stock_summary(abbreviation, option)
        for k, v in stock_dict.items():
            if k == 'Title':
                embed = discord.Embed(title=f'Summary for the stock of {v[0]}', colour=0xc27c0e, timestamp=now())
            else:
                try:
                    embed.add_field(name=k, value=v[0], inline=False)
                except IndexError:
                    pass
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='stocks_remind')
    async def stock_reminder_init(self, ctx, abbreviation, *user_days):
        """ Create a reminder for a stock """
        error_list = []
        days = ['m', 't', 'w', 'th', 'f']
        for i in user_days:
            if i not in days:
                error_list.extend(i)
        if len(error_list) > 0:
            ctx.send(f"Entered options of {', '.join(str(y) for y in error_list)} are not within weekdays abbreviated by {', '.join(str(y) for y in days)}")
        else:
            embed = discord.Embed(title='Reminder for stocks', colour=0xc27c0e, timestamp=now())
            embed.add_field(name=f"Reminder set for {abbreviation}", value=f"You will be messaged on {', '.join(str(y) for y in user_days)} at 4:00pm PDT", inline=False)
            await ctx.send(embed=embed)
            check = True
            while check:
                try:
                    with open(path('media', 'user_requests', 'reminders', 'stocks', ctx.message.author.id, f'{abbreviation}.txt'), 'w') as f:
                        f.write(' '.join(str(y) for y in user_days))
                        check = False
                except FileNotFoundError:
                    mkdir(path('media', 'user_requests', 'reminders', 'stocks', ctx.message.author.id))

    @comms.command(name='stocks_cancel')
    async def stock_reminder_cancel(self, ctx, abbreviation):
        """ Remove the reminder for the stock """
        os.remove(path('media', 'user_requests', 'reminders', 'stocks', ctx.message.author.id, f'{abbreviation}.txt'))

    """

    Background tasks

    """
    async def check_stock_reminders(self):
        """
        Checking folders for reminders then sending stock updates out
        """
        await self.bot.wait_until_ready()
        users = []
        for (dirpath, dirnames, filenames) in os.walk(path('media', 'user_requests', 'reminders', 'stocks')):
            users.extend(dirnames)
            break
        for user in users:
            user_request_abbreviations = []
            for (dirpath, dirnames, filenames) in os.walk(path('media', 'user_requests', 'reminders', 'stocks', user)):
                user_request_abbreviations.extend(filenames)
                break
            for i in range(len(user_request_abbreviations)):
                with open(path('media', 'user_requests', 'reminders', 'stocks', user, user_request_abbreviations[i])) as f:
                    if index_days(f.read().split(), datetime.datetime.today().weekday()):
                        stock_dict = get_stock_summary((user_request_abbreviations[i])[:-4])
                        for k, v in stock_dict.items():
                            if k == 'Title':
                                embed = discord.Embed(title=f'Summary for the stock of {v[0]}', colour=0xc27c0e, timestamp=now())
                            else:
                                try:
                                    embed.add_field(name=k, value=v[0], inline=False)
                                except IndexError:
                                    pass
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        for guild in self.bot.guilds:
                            for member in guild.members:
                                if member.id == int(user):
                                    user = member
                        await user.send(embed=embed)
                        printc(f"{now()}: {user.name}{user.discriminator} was reminded for {user_request_abbreviations[i]}")
        # while not self.bot.is_closed():
        #    if datetime.datetime.today().weekday() >= 0 and datetime.datetime.today().weekday() <= 4:
        #        if datetime.datetime.now().hour == 13:
        #            if datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
            # await asyncio.sleep(1)
            # print(f"{datetime.datetime.now()}: No events", end='\r')


def setup(bot):
    bot.add_cog(Reddit_Requester(bot))
    bot.add_cog(Weather_Requester(bot))
    bot.add_cog(Stock_Requester(bot))
