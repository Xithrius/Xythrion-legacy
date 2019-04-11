# ///////////////////////////////////////////////////////// #
# Logging
# ////////////////////////
# All errors are recorded in a .log file within the logs folder
# The file is .gitignore'd
# ///////////////////////////////////////////////////////// #


def discord_logger(default=False):
    if default:
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename=path('logs', 'discord.log'), encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
