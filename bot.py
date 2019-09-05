"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    First time usage:
        $ py -3 -m pip install --user -r requirements.txt
    To run the bot:
        $ py -3 bot.py

Todo:
    * Literally rewrite the repository

"""


import collections
import json

from discord.ext import commands as comms

from modules.output import path, ds


class Robot(comms.Bot):
    """."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #:
        with open(path('config', 'config.json'), 'r', encoding='utf8') as f:
            config = json.load(f)

        #:
        self.config = json.loads(json.dumps(config), object_hook=lambda d: collections.namedtuple('config', d.keys())(*d.values()))


class RobotCog(comms.Cog):
    """."""

    def __init__(self, bot):
        #:
        self.bot = bot
    
    @comms.command()
    async def exit(self, ctx):
        ds('[ Warning ]: Logging out.')
        await ctx.bot.logout()


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(RobotCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
