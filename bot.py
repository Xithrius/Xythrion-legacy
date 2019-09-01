"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    $ py -3 -m pip install --user -r requirements.txt
    $ py -3 bot.py

Todo:
    * Rewrite everything to match to PortgreSQL

"""


import collections
import json
import psycopg2
import configparser

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, get_cogs, ds


class Robot(comms.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=comms.when_mentioned_or('.'))

        with open(path('handlers', 'configuration', 'config.json'), 'r', encoding='utf8') as f:
            data = json.load(f)

        self.config = json.loads(json.dumps(data), object_hook=lambda d: collections.namedtuple("config", d.keys())(*d.values()))


class RecorderCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot
        if not os.path.isfile(self.bot.db_path):
            pass


class MainCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    async def exit(self, ctx):
        await ctx.bot.logout()


if __name__ == "__main__":
    bot = Robot()
    bot.add_cog(MainCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
