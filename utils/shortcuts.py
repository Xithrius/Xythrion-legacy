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
from datetime import datetime

import discord


def path(*filepath) -> str:
    """Returns absolute path from main caller file to another location.

    Args:
        filepath (iritable): Arguments to add to the current filepath.

    Returns:
        String of filepath with OS based seperator.

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
        A string with the current date for filename usage.

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
        a file and embed object.

    Examples:
        >>> embed_attachment(path('tmp', 'image.png'))

    """
    f = p.split(os.sep)[-1]
    file = discord.File(p, filename=f)
    embed = discord.Embed() if not embed else embed
    embed.set_image(url=f'attachment://{f}')
    return file, embed


def parallel_executor(func: t.Callable) -> t.Coroutine:
    """

    """

    async def run_blocking(func: functools.partial,
                           loop: asyncio.AbstractEventLoop,
                           executor: concurrent.futures.Executor):
        """

        """
        done, pending = await asyncio.wait(
            fs=(loop.run_in_executor(executor, func),),
            return_when=asyncio.FIRST_COMPLETED
        )

        return done.pop().result()

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> None:
        """

        """
        p_func = functools.partial(func, self, *args, **kwargs)
        result = await asyncio.ensure_future(
            run_blocking(p_func, self.bot.loop, self.bot.executor)
        )

        return result

    return wrapper


def content_parser() -> t.List[t.Tuple[str]]:
    pass


def tracebacker(e: Exception) -> None:
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
