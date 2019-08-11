"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sqlite3
import asyncio
import datetime

from discord.ext import commands as comms
import discord

from handlers.modules.output import now, path, printc


class Weather_Requester(comms.Cog):
    """ Get information from WeatherBit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Aiohttp session
        Required headers for requests
        """
        self.bot = bot

        # self.background_weather = self.bot.loop.create_task(self.collect_weather())

        if not os.path.isfile(self.bot.db_path):
            self.create_db()

        self.c = sqlite3.connect(self.bot.db_path)

    """ Permission checking """

    async def cog_check(self, ctx):
        """ """
        return all((ctx.message.author.id in self.bot.owner_ids, self.h))

    """ Databasing """

    def create_db(self):
        self.conn = sqlite3.connect(self.bot.db_path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE Weather (id INTEGER, time INTEGER, high INTEGER, low INTEGER, humidity INTEGER, sunrise INTEGER, sunset INTEGER)''')
        self.conn.commit()
        self.conn.close()

    """ Commands """


def setup(bot):
    bot.add_cog(Weather_Requester(bot))
