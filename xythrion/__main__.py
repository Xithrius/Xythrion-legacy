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
import logging

from .constants import Config


log = logging.getLogger(__name__)


# Creating the `tmp` directory if it doesn't exist
if not os.path.isdir(Path('tmp')):
    os.mkdir(Path('tmp'))

loop = asyncio.get_event_loop()


# Initializing the subclass of `comms.Bot`.
bot = Xythrion(
    command_prefix=comms.when_mentioned_or(';'),
    case_insensitive=True,
    help_command=None,
    loop=loop
)

# Attempting to run the bot (blocking, obviously).
try:
    bot.run(Config.TOKEN, bot=True, reconnect=True)

# If the token is incorrect or not given.
except discord.errors.LoginFailure:
    log.critical('Failed to startup bot: Improper token has been passed.')

except IndexError:
    log.critical('Could not index config file for discord token.')
