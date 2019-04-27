'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import datetime


"""

Functions for printing to locations with customized uniting

"""
def printc(string: str):
    """
    Customized printing to the console with timestamps
    """
    now = datetime.datetime.now()
    print(f"~> [{now}] {string}")


def duplicate(string: str):
    """
    Prints to console and wherever else
    """
    printc(string)
    return upper(string[string.index(':') + 2]) + lower(string[string.index(':') + 3])
