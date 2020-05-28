"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing as t


def codeblock(s: t.Union[str, list], language: str = 'py') -> str:
    """ """
    return f'```{0}\n{1}\n```'.format(
        language, '\n'.join(map(str, s)) if isinstance(s, list) else s
    )


def asteriks(s: str, amount: int = 3) -> str:
    """ """
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
