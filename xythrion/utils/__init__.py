"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from .markdown import asteriks, codeblock, markdown_link
from .shortcuts import (
    get_filename, parallel_executor, tracebacker, embed_attachment,
    describe_timedelta, fancy_embed, wait_for_reaction
)
from .tokenizer import tokenization


__all__ = [
    'strikethrough', 'bold', 'underline', 'asteriks', 'codeblock', 'single', 'markdown_link',
    'get_filename', 'embed_attachment', 'parallel_executor', 'tracebacker',
    'describe_timedelta', 'fancy_embed', 'wait_for_reaction', 'tokenization'
]
