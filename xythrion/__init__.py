"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import logging
import os
from pathlib import Path
from logging import handlers
import asyncio
import sys
import coloredlogs


logging.TRACE = 15
logging.addLevelName(logging.TRACE, 'TRACE')


def trace_logger(self: logging.Logger, msg: str, *args, **kwargs) -> None:
    """Log messages with the `TRACE` level."""
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, msg, args, **kwargs)


logging.Logger.trace = trace_logger

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'

log_formatter = logging.Formatter(LOG_FORMAT)

log_file = Path.cwd() / 'logs' / 'bot.log'
log_file.parent.mkdir(exist_ok=True)

file_handler = handlers.RotatingFileHandler(
    log_file,
    maxBytes=8388608,
    backupCount=7,
    encoding='utf-8'
)

file_handler.setFormatter(log_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
root_logger.addHandler(file_handler)

coloredlogs.DEFAULT_LEVEL_STYLES = {
    **coloredlogs.DEFAULT_LEVEL_STYLES,
    'trace': {'color': 246},
    'critical': {'background': 'red'},
    'debug': coloredlogs.DEFAULT_LEVEL_STYLES['info']
}

coloredlogs.DEFAULT_LOG_FORMAT = LOG_FORMAT

coloredlogs.install(logger=root_logger, stream=sys.stdout, level=logging.TRACE)

log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

if os.name == 'nt':
    log.info('Setting WindowsSelectorEventLoopPolicy as Snek is running on Windows')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
