"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import concurrent.futures
import functools
import os
import sys
import traceback
import typing as t
from datetime import datetime, timedelta

import discord
from discord.ext import commands as comms


def path(*filepath: t.Iterable[str]) -> str:
    """Returns absolute path from main caller file to another location.

    Args:
        filepath (:obj:`t.Iterable`): Arguments to add to the current filepath.

    Returns:
        str: filepath with OS based seperator.

    Examples:
        >>> print(path('tmp', 'image.png'))
        C:\\Users\\Xithr\\Documents\\Repositories\\Xythrion\\tmp\\image.png

    """
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


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


def embed_attachment(p: str, embed: discord.Embed = None) -> t.Tuple[discord.File, discord.Embed]:
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
        AttributeError: If `func` doesn't have attribute bot, and/or loop, executor.

    """
    async def run_blocking(func: functools.partial,
                           loop: asyncio.AbstractEventLoop,
                           executor: concurrent.futures.Executor) -> t.Any:
        """Inner function meant to wait for the executor to finish before returning results.

        Args:
            func (:obj:`functools.partial`): `func` as a callable with arguments.
            loop (:obj:`asyncio.AbstractEventLoop`): The loop for the executor to use.
            executor (:obj:`concurrent.futures.Executor`): The executor for the function to be ran in.

        Returns:
            :obj:`t.Any`: The object that `func` returns.

        Raises:
            AttributeError: Any exception will be silenced by the executor, unless the timeout occurs,
                which will cause the first result to not exist/contain anyhting.
            NOTE: Re-check if this is true, just in case.

        """
        done, pending = await asyncio.wait(
            fs=(loop.run_in_executor(executor, func),),
            loop=loop,
            timeout=20.0,
            return_when=asyncio.FIRST_COMPLETED
        )

        return done.pop().result()

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> t.Any:
        """The inner function, used for creating parallels so executors can run alongside eachother.

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

        p_func = functools.partial(func, self, *args, **kwargs)
        result = await asyncio.ensure_future(
            run_blocking(p_func, self.bot.loop, self.bot.executor)
        )

        return result

    return wrapper


def content_parser() -> t.List[t.Tuple[str]]:
    """Parses arguments from a string.

    NOTE: Currently not in use until the graphing extension is fixed.

    Returns:
        :obj:`t.List[t.Tuple[str]]`: A list of tuples that contain strings.

    """
    pass


def tracebacker(e: Exception) -> None:
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def describe_timedelta(d: timedelta) -> str:
    """ """
    timestamps = ['Hours', 'Minutes', 'Seconds']
    tmp = str((datetime.min + d).time()).split(':')

    return ', '.join(f'{int(float(tmp[i]))} {timestamps[i]}' for i in range(
        len(timestamps)) if float(tmp[i]) != 0.0)


def fancy_embed(d: t.Dict[str, t.List[str]], *,
                inline: bool = False, return_str: bool = False) -> t.Union[str, discord.Embed]:
    """ """

    d = {f'`{k}`\n': '\n'.join(str(y) for y in v) + '\n' for k, v in d.items()}
    d = '\n'.join(f'{k}{v}' for k, v in d.items())

    if not return_str:
        return discord.Embed(description=d)

    return d


async def wait_for_reaction(ctx: comms.Context, emoji) -> bool:
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == emoji

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

    except asyncio.TimeoutError:
        pass

    else:
        return True
