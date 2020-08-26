"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


import logging
import os
from pathlib import Path

import discord
from discord.ext.commands import when_mentioned_or
from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS

from .constants import Config


log = logging.getLogger(__name__)

if not os.path.isdir(Path('tmp')):
    os.mkdir(Path('tmp'))

bot = Xythrion(
    command_prefix=when_mentioned_or(';'),
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions(everyone=False)
)

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(Config.TOKEN, bot=True, reconnect=True)
