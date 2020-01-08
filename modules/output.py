"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import os
import datetime
import random


def path(*filepath) -> str:
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


class sp:
    """Status Print outputs date, status, and maybe a custom string."""

    @classmethod
    def insert_items(cls, warning, string) -> str:
        """
        Args:
            warning: string of what the warning should say
            string: description of the warning
        Returns:
            A string with a date, warning, and string.
        """
        rn = datetime.datetime.now()
        s = [
            f"[{rn.strftime('%A %I:%M:%S')}{rn.strftime('%p').lower()}]{':' if not warning else ''}",
            f'[ {warning} ]:' if warning else False,
            f'{string} '
        ]
        return ' '.join(str(y) for y in s if y)

    @classmethod
    def c(cls, *string):
        "Returns a custom warning with a string,"
        print(cls.insert_items(False, ' '.join(string)))

    @classmethod
    def w(cls, *string):
        """Returns a warning string."""
        print(cls.insert_items('Warning', ' '.join(string)))

    @classmethod
    def f(cls, *string):
        """Returns a fatal string."""
        print(cls.insert_items('Fatal', ' '.join(string)))

    @classmethod
    def s(cls, *string):
        """Returns a success string."""
        print(cls.insert_items('Success', ' '.join(string)))

    @classmethod
    def r(cls, *string):
        """Returns a custom warning string."""
        print(cls.insert_items('Ready', ' '.join(string)))


def get_extensions() -> list:
    return [f'cogs.{i[:-3]}' for i in os.listdir(path('cogs')) if i[-3:] == '.py']


def file_name() -> int:
    return int(datetime.datetime.timestamp(datetime.datetime.now()))
