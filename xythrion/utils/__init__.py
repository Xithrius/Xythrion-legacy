"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from .markdown import asteriks, codeblock, markdown_link
from .shortcuts import (
    get_filename, parallel_executor, tracebacker, embed_attachment,
    fancy_embed, wait_for_reaction, http_get, shorten
)
from .tokenizer import tokenize


__all__ = [
    'strikethrough', 'bold', 'underline', 'asteriks', 'codeblock', 'single', 'markdown_link',
    'get_filename', 'embed_attachment', 'parallel_executor', 'tracebacker',
    'fancy_embed', 'wait_for_reaction', 'tokenize', 'http_get', 'shorten'
]
