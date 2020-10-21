import logging

from discord import AllowedMentions
from discord.ext.commands import when_mentioned

from xythrion.bot import Xythrion
from xythrion.constants import Config
from xythrion.extensions import EXTENSIONS

log = logging.getLogger(__name__)

bot = Xythrion(
    command_prefix=when_mentioned,
    case_insensitive=True,
    help_command=None,
    allowed_mentions=AllowedMentions(everyone=False)
)

for extension in EXTENSIONS:
    bot.load_extension(extension)
    log.info(f'Loaded extension "{extension}"')

bot.run(Config.TOKEN, bot=True, reconnect=True)
