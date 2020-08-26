"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


import asyncio
from datetime import datetime
import functools
import os
from pathlib import Path
import typing as t

from discord import Embed, Emoji, File, Member, Message, TextChannel
from discord.ext.commands import BadArgument, Context, MessageConverter


def gen_filename() -> str:
    """Generates a filename from the current date."""
    return str(datetime.timestamp(datetime.now())).replace('.', '')


def embed_attachment(p: str, embed: t.Optional[Embed] = None) -> t.Tuple[File, Embed]:
    """Creating an embed and adding a local image to it."""
    f = p.split(os.sep)[-1]
    file = File(p, filename=f)
    embed = Embed() if not embed else embed

    embed.set_image(url=f'attachment://{f}')

    return file, embed


def shorten(s: str, approx_string_len: int = 10) -> str:
    """Shortens a string down to an amount of characters."""
    if len(s) < approx_string_len:
        return s

    return ' '.join(s[:approx_string_len + 1].split()[:-1]) + '...'


def parallel_executor(func: t.Callable) -> t.Any:
    """
    Wrapper for making synchronous functions awaitable.

    The synchronous function, after being turned into an asynchronous one, will only
    return after the function is complete.
    """
    async def exec_func(sync_func: t.Callable, loop: asyncio.AbstractEventLoop) -> t.Any:
        """Starting the executor and returning the response of the function."""
        res = await loop.run_in_executor(None, sync_func)

        return res

    @functools.wraps(func)
    async def wrapper(self: t.Generic, *args: t.Iterable[t.Any], **kwargs: t.Dict[t.Any, t.Any]) -> t.Any:
        """The inner function, used for creating tasks so executors can be ran."""
        if not isinstance(func, t.Callable):
            raise ValueError('Incorrect function type passed. Did not get synchronous.')

        func_partial = functools.partial(func, self, *args, **kwargs)
        res = await exec_func(func_partial, self.bot.loop)

        return res

    return wrapper


async def wait_for_reaction(ctx: Context, emoji: Emoji) -> bool:
    """Waiting for a user to react to a message sent by the bot."""
    def check(reaction: Emoji, user: Context.author) -> bool:
        return user == ctx.message.author and str(reaction.emoji) == emoji

    try:
        _, __ = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

    except asyncio.TimeoutError:
        pass

    else:
        return True


def calculate_lines() -> int:
    """Gets the sum of lines from all the python files a directory."""
    lst = []
    amount = 0

    for root, _, files in os.walk(Path.cwd()):
        for file in files:
            if file.endswith('.py'):
                lst.append(os.path.join(root, file))

    for file in lst:
        with open(file) as f:
            amount += sum(1 for _ in f)

    return amount


def permissions_in_channel(member: Member, channel: TextChannel, *permissions: str) -> bool:
    """Checks if a user has a permission(s) within a channel."""
    member_perms_in_channel = channel.permissions_for(member)
    return all(getattr(member_perms_in_channel, permission, False) for permission in permissions)


async def get_discord_message(
        ctx: Context, permissions: t.Iterable[str], text: str) -> t.Union[Message, bool]:
    """Converts a message ID or link to a message object."""
    try:
        msg = await MessageConverter().convert(ctx.channel, text)

        if permissions_in_channel(ctx.author, msg.channel, *permissions):
            return msg

        else:
            raise PermissionError

    except BadArgument:
        return False
