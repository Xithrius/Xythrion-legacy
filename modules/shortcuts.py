"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import functools

import discord

from modules.output import now


def embed(title, desc, fields=None, url=None):
    """Automating the creation of a discord.Embed with modifications.

    Returns:
        An embed object.

    """
    if isinstance(desc, dict):
        desc = [f'[`{k}`]({v})' for k, v in desc.items()]
    elif isinstance(desc, str):
        desc = [desc]
    elif isinstance(desc, list):
        pass
    else:
        desc.append(f'[`link`]({url})')
    e = discord.Embed(title=title, description='\n'.join(y for y in desc),
                        timestamp=now(), colour=0xc27c0e)
    if fields:
        for k, v in fields.items():
            e.add_field(name=k, value=v)
    e.set_footer(text=f'discord.py v{discord.__version__}',
                    icon_url='https://i.imgur.com/RPrw70n.png')
    return e


def partial_function(function, *args):
    """


    Example usage:
        func = partial_function(self.func, args)
        info = await self.bot.loop.run_in_executor(None, func)

    """
    
    return functools.partial(function, *args)
    
