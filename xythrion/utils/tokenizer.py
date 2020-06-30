"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools
import re
import typing as t
from collections import OrderedDict

from discord.ext import commands as comms

from . import parallel_executor


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


# print(parse('5*((x-2)*(x-3))'))


def tokenization(func: t.Union[t.Coroutine, t.Callable]) -> t.Coroutine:

    @parallel_executor
    def tokenizer(self, string: str) -> t.List[str]:
        """

        Examples:
            print(tokenizer('5*((x-2)*(x-3))'))

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

    @functools.wraps(func)
    async def wrapper(self, ctx: comms.Context, *, msg: str) -> t.Any:
        res = await tokenizer(self, msg)

        return res

    return wrapper
