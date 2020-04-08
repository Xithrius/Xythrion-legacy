"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from .conversion import (
    kelvin_to_fahrenheit, kelvin_to_celcius,
    celcius_to_kelvin, celcius_to_fahrenheit
)
from .shortcuts import (
    path, get_extensions, shorten,
    gen_block, http_get, gen_filename,
    describe_date, lock_executor, embed_attachment,
    ast, markdown_link, quick_block
)


__all__ = [
    'kelvin_to_fahrenheit', 'kelvin_to_celcius',
    'celcius_to_kelvin', 'celcius_to_fahrenheit',

    'path', 'get_extensions', 'shorten',
    'gen_block', 'http_get', 'gen_filename',
    'describe_date', 'lock_executor', 'embed_attachment',
    'ast', 'markdown_link', 'quick_block'
]
