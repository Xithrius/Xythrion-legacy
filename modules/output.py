"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import os
import datetime


def path(*filepath) -> str:
    """Returns absolute path from main caller file to another location.
    
    Args:
        filepath (iritable): Arguments to add to the current filepath.

    Returns:
        String of filepath with OS based seperator.

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

    """
    c = []
    
    for folder in os.listdir(path('cogs')):
        c.extend([f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py'])

    return c


def filename() -> str:
    """Generates a filename.
    
    Returns:
        A string with the current date for filename usage.

    """
    return str(datetime.datetime.timestamp(datetime.datetime.now()))


def shorten(s: str, char_limit=50) -> str:
    """Cuts down a string to a specific length and adds '...'

    Args:
        s (str): The input string
        _len (int): The desired limit for length

    Returns:
        A string cut down to a specific length.

    """
    new_str = []
    for word in s.strip().split():
        if len(' '.join(str(y) for y in new_str)) < char_limit:
            new_str.append(word)
        else:
            break

    new_str = ' '.join(str(y) for y in new_str).strip()
    return new_str + '...' if len(new_str) >= char_limit else new_str
