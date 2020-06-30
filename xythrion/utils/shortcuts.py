"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import functools
import os
import sys
import traceback
import typing as t
from datetime import datetime, timedelta

import discord
from discord.ext import commands as comms


def get_filename() -> str:
    """Generates a filename.

    Returns:
        str: The current date for filename usage.

    Examples:
        >>> print(gen_filename())
        1584774125328021

        >>> print(f'{gen_filename()}.png')
        1584774141733494.png

    """
    return str(datetime.timestamp(datetime.now())).replace('.', '')


def embed_attachment(p: str, embed: t.Optional[discord.Embed] = None) -> t.Tuple[discord.File, discord.Embed]:
    """Creating an embed and adding a local image to it.

    Args:
        p (str): The absolute path for the file of the image.

    Returns:
        :obj:`t.Tuple[discord.File, discord.Embed]`: A file and an embed object.

    Examples:
        >>> embed_attachment(path('tmp', 'image.png'))

    """
    f = p.split(os.sep)[-1]
    file = discord.File(p, filename=f)
    embed = discord.Embed() if not embed else embed

    embed.set_image(url=f'attachment://{f}')

    return file, embed


def parallel_executor(func: t.Callable) -> t.Coroutine:
    """Wrapper for making synchronous functions awaitable.

    The synchronous function, after being turned into an asynchronous one, will only
    return after the function is complete.

    Args:
        func (:obj:`t.Callable`): The synchronous function to be ran.

    Returns:
        :obj:`t.Coroutine`: The asynchronous function.

    Raises:
        ValueError: If the passed in function is not synchronous.
        AttributeError: If `func` doesn't have attribute bot, and/or loop.

    """

    async def exec_func(func, loop) -> t.Any:
        """Starting the executor and returning the response of the function.

        Inner function meant to wait for the executor to finish before returning results.

        Args:
            func (:obj:`functools.partial`): `func` as a callable with arguments.
            loop (:obj:`asyncio.AbstractEventLoop`): The loop for the executor to use.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            :obj:`t.Any`: The object that `func` returns.

        Raises:
            None. All exceptions are silenced by the executor.

        """
        res = await loop.run_in_executor(None, func)

        return res

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> t.Any:
        """The inner function, used for creating tasks so executors can be ran.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            :obj:`t.Any`: The object that `func` returns.

        Raises:
            ValueError: If the passed in function is not synchronous.

        """
        if not isinstance(func, t.Callable):
            raise ValueError('Incorrect function type passed. Did not get synchronous.')

        func_partial = functools.partial(func, self, *args, **kwargs)
        res = await exec_func(func_partial, self.bot.loop)

        return res

    return wrapper


def tracebacker(e: Exception) -> None:
    """Safely gives a traceback of an exception letting the rest of the program flow.

    Args:
        e (Exception): The exception that was raised.

    Returns:
        bool: Always None.

    Raises:
        AttributeError: If the exception is not derived from the Exception base class.

    """
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def describe_timedelta(d: timedelta) -> str:
    """Describing a timedelta in possibily the most conviluted way.

    Args:
        d (:obj:`datetime.timedelta`): The difference between one datetime.datetime object and another.

    Returns:
        str: Contains hours and/or minutes, seconds for describing the difference between two dates.

    Raises:
        ValueError: If the only argument passed is not a `datetime.timedelta` object.

    """
    timestamps = ['Hours', 'Minutes', 'Seconds']
    tmp = str((datetime.min + d).time()).split(':')

    return ', '.join(f'{int(float(tmp[i]))} {timestamps[i]}' for i in range(
        len(timestamps)) if float(tmp[i]) != 0.0)


def fancy_embed(d: t.Dict[str, t.List[str]], *,
                inline: bool = False, return_str: bool = False) -> t.Union[str, discord.Embed]:
    """Creating an embed only with the description. No fields or titles needed.

    Args:
        d (:obj:`t.Dict[str, t.List[str]]`): A dictionary with strings as keys and lists of strings as values.
        inline (bool, optional): If inline is wanted to be used within the embed.
        return_str (boo, optional): Returning the description contents instead of the embed if True.

    Returns:
        :obj:`t.Union[str, discord.Embed]`: Either an embed or the description contents.

    """
    d = {f'`{k}`\n': '\n'.join(str(y) for y in v) + '\n' for k, v in d.items()}
    d = '\n'.join(f'{k}{v}' for k, v in d.items())

    if not return_str:
        return discord.Embed(description=d, inline=inline)

    return d


async def wait_for_reaction(ctx: comms.Context, emoji) -> bool:
    """Waiting for a user to react to a message sent by the bot.

    NOTE: Obviously not a wrapper.

    Args:
        ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
        emoji (str): Unicode representing an emoji that can be used by Discord.

    Raises:
        UnicodeError: If the emoji unicode cannot be read properly.

    """
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == emoji

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

    except asyncio.TimeoutError:
        pass

    else:
        return True
