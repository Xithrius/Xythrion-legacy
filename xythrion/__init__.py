"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import logging
import os
import typing as t
from pathlib import Path
from rich import logging as r_logging


def _discord_logger(log_type: t.Optional[t.Union[str, int]] = None) -> logging.Logger:
    """Logs information specifically for discord.

    Args:
        log_type (:obj:`t.Union[str, int]`, optional): The level of logging to be used.
            Defaults to None.

    Returns:
        :obj:`logging.Logger`: The object that the bot will use to log information to.

    """
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    if not os.path.isdir(Path(f'tmp{os.sep}')):
        os.mkdir(Path('tmp'))

    base_handler = logging.FileHandler(filename=Path('tmp', 'discord.log'), encoding='utf-8', mode='w')
    base_handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(base_handler)

    return logger


def _rich_logger(log_type: int = 20) -> logging.Logger:
    """Logs information with the rich library with fancy tracebacks.

    Args:
        log_type (:obj:`t.Union[str, int]`, optional): The level of logging to be used.
            Defaults to None.
        store_file (bool, optional): If the logs want to be stored.

    Returns:
        :obj:`logging.Logger`: The object that the bot will use to log information to.

    Raises:
        IndexError: If `log_type` isn't within log_types.

    """
    logging.basicConfig(
        level=log_type, format='%(message)s', datefmt="[%c]", handlers=[r_logging.RichHandler()]
    )

    # different message types: info, debug, warning, critical
    return logging.getLogger('rich')
