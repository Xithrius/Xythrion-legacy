"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import json
import aiohttp
import random
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import printc, path, now


class Osu_Requester(comms.Cog):
    """ Get information from WeatherBit """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Aiohttp session
        Required headers for requests
        """
        self.bot = bot
        self.s = aiohttp.ClientSession()
        self.h = self.bot.services[os.path.basename(__file__)[:-3]]

    """ Cog events """

    async def cog_unload(self):
        self.bot.loop.create_tank(self.s.close())

        """ Permission checking """

        async def cog_check(self, ctx):
            """ """
            # _is_owner = ctx.message.author.id in self.bot.config['owners']
            # return all((_is_owner, self.h))
            return if self.h

    """ Commands """


def setup(bot):
    bot.add_cog(Osu_Requester(bot))
