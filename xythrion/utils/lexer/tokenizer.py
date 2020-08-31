import re
from collections import OrderedDict
from typing import List, Tuple

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


def parse(string: str) -> List[Tuple[str]]:
    """
    Parsing the string into tokens.

    Example: print(parse('5*((x-2)*(x-3))')).
    """
    string = re.sub(re.compile(r'\s+'), '', string)

    tokens = []

    while string:
        for name, pattern in TOKENTYPES.items():
            m = re.match(pattern, string)
            if m is not None:
                tokens.append((name, m.group(0)))
                string = string[len(m.group(0)):]
                break

        else:
            raise ValueError('Input string could be not parsed correctly.')

    return tokens
