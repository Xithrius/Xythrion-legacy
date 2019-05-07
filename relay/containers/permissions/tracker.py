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


import sys

from relay.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Tracker for permissions
# //////////////////////////////////////////////////////////////////////////// #
# Returns different booleans depending on the 
# //////////////////////////////////////////////////////////////////////////// #


def permitted():
    def wrapper(*args, **kwargs):
        print(*args, **kwargs)
    return wrapper