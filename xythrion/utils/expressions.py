import re
from collections import OrderedDict
from typing import Iterator, List, Tuple

TOKEN_TYPES = OrderedDict((
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


class TokenizationError(Exception):
    """Custom exception when failing parses."""

    def __init__(self, message: str, *args) -> None:
        super().__init__(message, *args)


class Tokenizer:
    """Creating tokens out of strings."""

    def __init__(self, expression: str) -> None:
        self.tokens = self.parse_string_into_tokens(expression)

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(self.tokens)

    @staticmethod
    def parse_string_into_tokens(expression: str) -> List[Tuple[str, str]]:
        """Parsing the given expression into tokens."""
        ex = re.sub(re.compile(r'\s+'), '', expression)

        tokens = []

        while ex:
            for name, pattern in TOKEN_TYPES.items():
                m = re.match(pattern, ex)
                if m is not None:
                    tokens.append((name, m.group(0)))
                    ex = ex[len(m.group(0)):]
                    break

            else:
                raise TokenizationError('Input string could be not tokenized correctly.')

        return tokens
