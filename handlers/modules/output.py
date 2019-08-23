"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import __main__
import datetime
import os
import asyncio


def path(*_items):
    """ Gives a path relative to caller file location with added items.

    Args:
        objects: An amount of different items to path to as strings.

    Returns:
        A Path joined by the operating system's seperator.

    """
    newPath = ((__main__.__file__).split(os.sep))[:-1]
    for i in _items:
        newPath.append(i)
    return (os.sep).join(str(y) for y in newPath)


def now():
    """Returns the time depending on time zone from file

    Returns:
        The current date down to the milisecond.

    """
    return datetime.datetime.now()


def ds(string, end=False):
    """(AKA date_string) Returning a customized string with a timestamp that includes the date.

    Args:
        string: Just a regular string.

    Returns:
        A string with the current date within square brackets.

    """
    if not end:
        print(f"[{now()}] {string}")
    else:
        print(f"[{now()}] {string}", end=end)


def get_cogs(blocked_cogs):
    """Gets cog filepaths within the 'cogs' folder

    Args:
        blocked_cogs: A list of cogs that are not allowed to be loaded

    Returns:
        A list of strings with filepaths joined by a '.'

    """
    folders = [folder for folder in os.listdir(path('cogs')) if folder != '__pycache__']
    exts = []
    for folder in folders:
        folder_cogs = [f'cogs.{folder}.{cog[:-3]}' for cog in os.listdir(path('cogs', folder)) if os.path.isfile(path('cogs', folder, cog)) and cog[:-3] not in blocked_cogs]
        exts.extend(folder_cogs)
    return exts


def get_filename(id, end=''):
    """Here's a specific, random file name.

    Args:
        id: The ID of a user
        end: The format of the file

    Returns:
        A string with the current date, id of a user, and the format of the file (if any)

    """
    return f'{int(datetime.datetime.timestamp((now())))}-{id}{end}'
