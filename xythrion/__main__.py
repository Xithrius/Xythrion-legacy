from discord import AllowedMentions
from loguru import logger as log

from xythrion.bot import Xythrion
from xythrion.constants import Config
from xythrion.extensions import EXTENSIONS

bot = Xythrion(
    command_prefix="\\",
    case_insensitive=True,
    help_command=None,
    allowed_mentions=AllowedMentions(everyone=False),
)

for extension in EXTENSIONS:
    bot.load_extension(extension)
    log.info(f'Loaded extension "{extension}"')

bot.run(Config.TOKEN)
