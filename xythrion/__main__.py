from disnake import AllowedMentions
from loguru import logger as log

from .bot import Xythrion
from .extensions import EXTENSIONS

import toml
from pathlib import Path

if not Path.is_file(Path.cwd() / "config.toml"):
    raise FileNotFoundError(f"{Path.cwd() / 'config.toml'} cannot be found as is required.")

config = toml.load(Path.cwd() / "config.toml")

bot = Xythrion(
    command_prefix="\\",
    case_insensitive=True,
    help_command=None,
    allowed_mentions=AllowedMentions(everyone=False),
)

for extension in EXTENSIONS:
    bot.load_extension(extension)
    log.info(f'Loaded extension "{extension}"')

bot.run(config["token"])
