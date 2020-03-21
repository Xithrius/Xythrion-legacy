"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime
import os
import sys


def path(*filepath) -> str:
    """Returns absolute path from main caller file to another location.

    Args:
        filepath (iritable): Arguments to add to the current filepath.

    Returns:
        String of filepath with OS based seperator.

    Examples:
        >>> print(path('tmp', 'image.png'))
        C:\\Users\\Xithr\\Documents\\Repositories\\Xythrion\\tmp\\image.png

    """
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


def get_extensions() -> list:
    """Gets all the extensions within a folder for the bot to load.

    Returns:
        a list of cogs starting with cogs.<folder if any>.<filename without .py>.

    Examples:
        >>> print(get_extensions())
        ['cogs.math.calculator', 'cogs.math.graphing', 'cogs.meta.custom']

    """
    c = []

    for folder in os.listdir(path('cogs')):
        c.extend([f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py'])

    return c


def gen_filename() -> str:
    """Generates a filename.

    Returns:
        A string with the current date for filename usage.

    Examples:
        >>> print(gen_filename())
        1584774125328021

        >>> print(f'{gen_filename()}.png')
        1584774141733494.png

    """
    return str(datetime.datetime.timestamp(datetime.datetime.now())).replace('.', '')


def shorten(s: str, char_limit: int = 50) -> str:
    """Cuts down a string to a specific length and adds '...'

    Args:
        s (str): The input string
        char_limit (int): The desired limit for length

    Returns:
        A string cut down to a specific length.

    Examples:
        >>> print(shorten("A large string that's very very very long and pretty much never ending until now"))
        A large string that's very very very long and pretty...

        >>> print(shorten("A large string that's very very very long."))
        A large string that's very very very long.

    """
    new_str = []
    for word in s.strip().split():
        if len(' '.join(str(y) for y in new_str)) < char_limit:
            new_str.append(word)
        else:
            break

    new_str = ' '.join(str(y) for y in new_str).strip()
    return new_str + '...' if len(new_str) >= char_limit else new_str
