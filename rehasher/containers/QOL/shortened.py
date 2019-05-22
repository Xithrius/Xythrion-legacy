'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import datetime


"""

Functions for returning shortened versions of longer functions

"""


def now():
    """
    Returns the time depending on time zone (will look at file soon)
    """
    return datetime.datetime.now() + datetime.timedelta(hours=7)


def index_days(lst: list, day: int):
    """
    Converting days to numerical values
    """
    days = ['m', 't', 'w', 'th', 'f']
    if days[day] in lst:
        return True
