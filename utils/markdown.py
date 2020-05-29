"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing as t


def codeblock(s: t.Union[str, t.List[str]], language: t.Union[str, None] = 'py') -> str:
    """Creates a codeblock for discord's markdown langauage.

    Args:
        s (:obj:`t.Union[str, t.List[str]]`): The string or list of string to be put into the codeblock.
        language (t.Union[str, None], optional): The language that the strings will be markdowned in, if any.

    Returns:
        str: An amount of strings surrounded by ```, with/without a defined programming language.

    Example(s):
        >>> print(codeblock('this thing here'))
        ```py
        this thing here
        ```

        >>> print(codeblock(['this thing here', 'that thing there'], 'c'))
        ```c
        this thing here
        that thing there
        ```

    """
    return f'```{0}\n{1}\n```'.format(
        language if language else '', '\n'.join(map(str, s)) if isinstance(s, list) else s
    )


def asteriks(s: str, amount: int = 3) -> str:
    """Surrounds a string in specified amounts of '*'

    Args:
        s (str): The string to be surrounded.
        amount (int): The amount of asteriks on both sides.

    Returns:
        str: Asterisk-surrounded string.

    Example(s):
        >>> print(asteriks('something'))
        ***something***

    """
    return f'{"*" * amount}{s}{"*" * amount}'


def markdown_link(s: str, link: str) -> str:
    """Gets rid of the thinking while creating a link for markdown.

    Args:
        s (str): The name of the link that will be shown
        link (str): The link that the link will link to.

    Returns:
        A string containing the format of a markdown link (ex. a .md file.)

    Examples:
        >>> print(markdown_link('Google', 'https://google.com'))
        [`Google`](https://google.com)

    """
    return f'[`{s}`]({link})'
