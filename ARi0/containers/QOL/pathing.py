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


import __main__

from distutils import dir_util
import platform
import os


"""

Relative creation of objects

"""


def path(*objects):
    """
    Returns path relative to caller file location with additional objects, if any
    """
    newPath = ((__main__.__file__).split(os.sep))[:-1]
    for i in objects:
        newPath.append(i)
    return (os.sep).join(str(y) for y in newPath)


def create_dir(*objects):
    """
    Creats a new folder at a given location
    """
    dir_util.mkpath(path(*objects))
