import logging
from os import listdir, mkdir, remove
from pathlib import Path

import discord
from discord.ext.commands import when_mentioned_or

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from .constants import Config

if not Path.cwd().exists:
    mkdir(Path.cwd() / 'tmp')

log = logging.getLogger(__name__)

log.info('Cleaning out tmp/...')
for file in listdir(Path.cwd() / 'tmp'):
    remove(Path.cwd() / 'tmp' / file)

bot = Xythrion(
    description=Config.BOT_DESCRIPTION,
    command_prefix=when_mentioned_or('\\'),
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions(everyone=False)
)

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(Config.TOKEN, bot=True, reconnect=True)
