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


import os
import datetime
import platform

import discord
from discord.ext import commands as comms

from scraping.yahoo_finance import get_stock_summary
from essentials.converter import index_days
from essentials.pathing import path, mkdir


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class StockCog(comms.Cog):

    # //////////////////////////////////////////////// # Attribute creation
    # //////////////////////// # Objects: bot and background task
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_stock_reminders())

    # //////////////////////// # Cancel background task when cog is unloaded
    def cog_unload(self):
        self.bg_task.cancel()

# //////////////////////////////////////////////// # Commands
# //////////////////////// # Get the current stock of something
    @comms.command(name='stocks')
    async def get_current_stocks(self, ctx, abbreviation, option='low'):
        stock_dict = get_stock_summary(abbreviation, option)
        for k, v in stock_dict.items():
            if k == 'Title':
                embed = discord.Embed(title=f'Summary for the stock of {v[0]}', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))
            else:
                try:
                    embed.add_field(name=k, value=v[0], inline=False)
                except IndexError:
                    pass
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

# //////////////////////// # Create a reminder for a stock
    @comms.command(name='stocks_remind')
    async def stock_reminder_init(self, ctx, abbreviation, *user_days):
        error_list = []
        days = ['m', 't', 'w', 'th', 'f']
        for i in user_days:
            if i not in days:
                error_list.extend(i)
        if len(error_list) > 0:
            ctx.send(f"Entered options of {', '.join(str(y) for y in error_list)} are not within weekdays abbreviated by {', '.join(str(y) for y in days)}")
        else:
            embed = discord.Embed(title='Reminder for stocks', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))
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

# //////////////////////// # Remove the reminder for the stock
    @comms.command(name='stocks_cancel')
    async def stock_reminder_cancel(self, ctx, abbreviation):
        os.remove(path('media', 'user_requests', 'reminders', 'stocks', ctx.message.author.id, f'{abbreviation}.txt'))

# //////////////////////////////////////////////// # Background tasks
# //////////////////////// # Checking folders for reminders then sending stock updates out
    async def check_stock_reminders(self):
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
                                embed = discord.Embed(title=f'Summary for the stock of {v[0]}', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))
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
                        print(f"{datetime.datetime.now()}: {user.name}{user.discriminator} was reminded for {user_request_abbreviations[i]}")
        # while not self.bot.is_closed():
        #    if datetime.datetime.today().weekday() >= 0 and datetime.datetime.today().weekday() <= 4:
        #        if datetime.datetime.now().hour == 13:
        #            if datetime.datetime.now().minute == 0 and datetime.datetime.now().second == 0:
            # await asyncio.sleep(1)
            # print(f"{datetime.datetime.now()}: No events", end='\r')


def setup(bot):
    bot.add_cog(StockCog(bot))
