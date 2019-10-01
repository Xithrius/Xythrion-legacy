"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import __main__
import datetime
import os
import asyncio
import math

from uszipcode import SearchEngine


def path(*_items):
    """Gives a path relative to caller file location with added items.

    Args:
        objects: An amount of different items to path to as strings.

    Returns:
        A Path joined by the operating system's seperator.

    """
    newPath = ((__main__.__file__).split(os.sep))[:-1]
    for i in _items:
        newPath.append(i)
    return (os.sep).join(str(y) for y in newPath)


class cs:
    """A string including another thing, automated."""

    @classmethod
    def insert_items(cls, warning, string):
        """

        Args:
            warning: string of what the warning should say
            string: description of the warning

        Returns:
            A string with a date, warning, and string.

        """
        rn = now()
        return f"[{rn.strftime('%A %I:%M:%S')}{rn.strftime('%p').lower()}] [ {warning} ]: {string}"

    @classmethod
    def insert_block(cls, language, warning, string):
        return f'```{language}\n{warning} {string}\n```'

    @classmethod
    def w(cls, string):
        """Returns a warning string."""
        print(cls.insert_items('Warning', string))

    @classmethod
    def f(cls, string):
        """Returns a fatal string."""
        print(cls.insert_items('Fatal', string))

    @classmethod
    def s(cls, string):
        """Returns a success string."""
        print(cls.insert_items('Success', string))

    @classmethod
    def r(cls, string):
        """Returns a custom warning string."""
        print(cls.insert_items('Ready', string))

    @classmethod
    def css(cls, string):
        """Returns a block quote containing css colour-coded words."""
        return cls.insert_block('css', '--!>', string)


def now():
    """Returns the time depending on time zone from file

    Returns:
        The current date down to the milisecond.

    """
    return datetime.datetime.now()


def get_extensions(blocked_extensions):
    """Gets extension filepaths within the 'cogs' folder

    Args:
        blocked_cogs: A list of extensions that are not allowed to be loaded

    Returns:
        A list of strings with filepaths joined by a '.'

    """
    folders = [folder for folder in os.listdir(path('cogs')) if folder != '__pycache__']
    exts = []
    for folder in folders:
        folder_cogs = [f'cogs.{folder}.{cog[:-3]}' for cog in os.listdir(path('cogs', folder)) if os.path.isfile(path('cogs', folder, cog)) and cog[:-3] not in blocked_extensions]
        exts.extend(folder_cogs)
    return exts


def get_filename(id, e=''):
    """Here's a specific, random file name.

    Args:
        id: The ID of a user
        e: The format of the file

    Returns:
        A string with the current date, id of a user, and the format of the file (if any)

    """
    return f'{int(datetime.datetime.timestamp((now())))}-{id}{e}'


def convert_coords(postal_code, z):
    """Converts postal code and zoom level to coordinates for the openweathermap API

    Args:
        postal_code: The postal code within the US
        z: Zoom level into the map.

    Returns:
        List of arguments to be put into a map

    Source:
        https://developer.here.com/documentation/map-tile/common/map_tile/topics/mercator-projection.html

    """
    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(str(postal_code))
    lat = zipcode.lat
    lon = zipcode.lng

    latRad = lat * math.pi / 180
    n = math.pow(2, z)

    x = n * ((lon + 180) / 360)
    y = n * (1 - (math.log(math.tan(latRad) + 1 / math.cos(latRad)) / math.pi)) / 2

    return [x, y]

    '''
    latRad = lat * Math.PI / 180;
    n = Math.pow(2, z);
    xTile = n * ((lon + 180) / 360);
    yTile = n * (1-(Math.log(Math.tan(latRad) + 1/Math.cos(latRad)) /Math.PI)) / 2;
    '''
