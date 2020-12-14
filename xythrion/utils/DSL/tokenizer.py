import re
from collections import OrderedDict
from typing import List, Tuple

from .errors import TokenizationError

TOKEN_TYPES = OrderedDict(
    (
        ("OPEN_PAREN", r"^\(|\["),
        ("CLOSE_PAREN", r"^\)|\]"),
        ("ADD", r"^\+"),
        ("SUBTRACT", r"^-"),
        ("MULTIPLY", r"^\*"),
        ("DIVIDE", r"^\/"),
        ("EXPONENTIAL", r"^\^"),
        ("NUMBER", r"^-?\d+\.?\d*"),
        ("VARIABLE", r"^[a-zA-Z_]+"),
    )
)


def parse(expression: str) -> List[Tuple[str, str]]:
    """Parsing the given expression into tokens."""
    ex = re.sub(re.compile(r"\s+"), "", expression)

    tokens = []

    while ex:
        for name, pattern in TOKEN_TYPES.items():
            m = re.match(pattern, ex)
            if m is not None:
                tokens.append((name, m.group(0)))
                index = len(m.group(0))
                ex = ex[index:]
                break

        else:
            raise TokenizationError("Input string could be not tokenized correctly.")

    return tokens
