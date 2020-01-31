"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import os
import datetime
import random

import modules.colors as c


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


class status:
    """Status Print outputs date, status, and maybe a custom string."""

    @classmethod
    def insert_items(cls, warning, string) -> str:
        """Inserting colors and dates into warning string.

        Args:
            warning: string of what the warning should say
            string: description of the warning
        
        Returns:
            A string with a date, warning, and string.
        
        """
        _now = datetime.datetime.now()
        s = [
            f"{c.BOLD}[{c.END} {c.DATE}{_now.strftime('%b %d, %Y - %A %I:%M:%S')}{_now.strftime('%p').lower()} {c.END}{c.BOLD}]{c.END}{':' if not warning else ''}",
            f'{c.BOLD}[{c.END} {warning} {c.BOLD}]{c.END}:' if warning else False,
            f'{string} '
        ]
        return ' '.join(str(y) for y in s if y)

    @classmethod
    def w(cls, *string):
        """Returns a warning string."""
        print(cls.insert_items(f'{c.WARNING}Warning{c.END}', ' '.join(string)))

    @classmethod
    def f(cls, *string):
        """Returns a fatal string."""
        print(cls.insert_items(f'{c.FAIL}Fatal{c.END}', ' '.join(string)))

    @classmethod
    def s(cls, *string):
        """Returns a success string."""
        print(cls.insert_items(f'{c.OKG}Success{c.END}', ' '.join(string)))

    @classmethod
    def r(cls, *string):
        """Returns a custom warning string."""
        print(cls.insert_items(f'{c.HEADER}Ready{c.END}', ' '.join(string)))


def get_extensions() -> list:
    """Gets all the extensions within a folder for the bot to load.
    
    Returns:
        a list of cogs starting with cogs.<folder if any>.<filename without .py>.

    """
    return [f'cogs.{i[:-3]}' for i in os.listdir(path('cogs')) if i[-3:] == '.py']


def file_name() -> str:
    """Generates a filename.
    
    Returns:
        A string with the current date for filename usage.

    """
    return str(datetime.datetime.timestamp(datetime.datetime.now()))
