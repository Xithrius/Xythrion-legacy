"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from typing import NamedTuple
import os


__all__ = (
    'Config',
)


class Config(NamedTuple):
    TOKEN = os.environ.get('BOT_TOKEN')
