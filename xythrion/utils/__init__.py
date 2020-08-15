"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from .markdown import codeblock, markdown_link
from .shortcuts import gen_filename, embed_attachment, shorten, wait_for_reaction

__all__ = [
    'codeblock', 'markdown_link',
    'gen_filename', 'embed_attachment', 'shorten', 'wait_for_reaction'
]
