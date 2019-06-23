'''
>> SoftBot.py
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
    return f'{datetime.datetime.now() + datetime.timedelta(hours=7)}'
