"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import os


def path(*filepath):
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)
