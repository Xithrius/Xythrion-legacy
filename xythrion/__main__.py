import logging

import discord
from discord.ext.commands import when_mentioned_or

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from .constants import BasicConfig, Config

log = logging.getLogger(__name__)

bot = Xythrion(
    description=BasicConfig.BOT_DESCRIPTION,
    command_prefix=when_mentioned_or(';'),
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions(everyone=False)
)

for extension in EXTENSIONS:
    bot.load_extension(extension)

bot.run(Config.TOKEN, bot=True, reconnect=True)
