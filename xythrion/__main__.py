"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import os
from pathlib import Path

import discord
from discord.ext import commands as comms

from xythrion.bot import Xythrion

from . import _rich_logger

# Creating the `tmp` directory if it doesn't exist
if not os.path.isdir(Path('tmp')):
    os.mkdir(Path('tmp'))

loop = asyncio.get_event_loop()

# Initializing the subclass of `comms.Bot`.
bot = Xythrion(
    command_prefix=comms.when_mentioned_or(';'),
    case_insensitive=True,
    help_command=None,
    log=_rich_logger(),
    loop=loop
)

# Attempting to run the bot (blocking, obviously).
try:
    bot.run(bot.config['discord'], bot=True, reconnect=True)

# If the token is incorrect or not given.
except discord.errors.LoginFailure:
    bot.log.critical('Failed to startup bot: Improper token has been passed.')

except IndexError:
    bot.log.critical('Could not index config file for discord token.')
