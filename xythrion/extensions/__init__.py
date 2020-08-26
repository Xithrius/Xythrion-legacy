"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from pkgutil import iter_modules

EXTENSIONS = frozenset(
    extension.name for extension in iter_modules(('xythrion/extensions',), 'xythrion.extensions.')
)
