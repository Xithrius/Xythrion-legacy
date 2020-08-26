"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from collections import OrderedDict
import re
from typing import List

TOKENTYPES = OrderedDict((
    ('OPEN_PAREN', r'^\(|\['),
    ('CLOSE_PAREN', r'^\)|\]'),
    ('ADD', r'^\+'),
    ('SUBTRACT', r'^-'),
    ('MULTIPLY', r'^\*'),
    ('DIVIDE', r'^\/'),
    ('EXPONENTIAL', r'^\^'),
    ('NUMBER', r'^-?\d+\.?\d*'),
    ('VARIABLE', r'^[a-zA-Z_]+')
))


def tokenize(string: str) -> List[str]:
    """
    Attempting to parse a string to prepare for plotting.

    print(tokenizer('5*((x-2)*(x-3))'))
    https://docs.python.org/3/library/tokenize.html#examples
    print(parse('5*((x-2)*(x-3))'))
    """
    tokens = []

    while string:
        for name, pattern in TOKENTYPES.items():
            m = re.match(pattern, string)

            if m is not None:
                tokens.append((name, m.group(0)))

                string = string[len(m.group(0)):]

                break

        else:
            raise ValueError('Bad math, dumbass. Git gud.')

    return tokens
