"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import functools
import os
import typing as t
from datetime import datetime

from discord import File, Embed
from discord.ext.commands import Context


def gen_filename() -> str:
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


def embed_attachment(p: str, embed: t.Optional[Embed] = None) -> t.Tuple[File, Embed]:
    """Creating an embed and adding a local image to it.

    Args:
        p (str): The absolute path for the file of the image.

    Returns:
        :obj:`t.Tuple[discord.File, discord.Embed]`: A file and an embed object.

    Examples:
        >>> embed_attachment(path('tmp', 'image.png'))

    """
    f = p.split(os.sep)[-1]
    file = File(p, filename=f)
    embed = Embed() if not embed else embed

    embed.set_image(url=f'attachment://{f}')

    return file, embed


def shorten(s: str, mininum_character_count: int = 10) -> str:
    """ """
    if len(s) < mininum_character_count:
        return s

    return ' '.join(s[:mininum_character_count + 1].split()[:-1]) + '...'


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


async def wait_for_reaction(ctx: Context, emoji) -> bool:
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
