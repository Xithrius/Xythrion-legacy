"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from .markdown import code_block, markdown_link
from .shortcuts import (calculate_lines, embed_attachment, gen_filename,
                        get_discord_message, parallel_executor,
                        permissions_in_channel, shorten, wait_for_reaction)

__all__ = (
    'code_block', 'markdown_link', 'gen_filename',

    'embed_attachment', 'shorten', 'wait_for_reaction', 'parallel_executor', 'calculate_lines',
    'permissions_in_channel', 'get_discord_message'
)
