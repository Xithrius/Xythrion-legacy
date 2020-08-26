"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


import typing as t


def code_block(s: t.Union[str, t.List[str]], language: t.Union[str, None] = 'py') -> str:
    """Creates a code block for Discord's markdown language."""
    return f'```{0}\n{1}\n```'.format(
        language if language else '', '\n'.join(map(str, s)) if isinstance(s, list) else s
    )


def markdown_link(s: str, link: str) -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    return f'[`{s}`]({link})'
