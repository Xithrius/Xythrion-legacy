import asyncio
import logging
import os
import typing as t
from datetime import datetime
from pathlib import Path

import aiohttp
import asyncpg
from discord import Embed, Emoji, File, Member, Message, TextChannel
from discord.ext.commands import BadArgument, Context, MessageConverter

from xythrion.constants import Config
from xythrion.utils.markdown import markdown_link

log = logging.getLogger(__name__)


def gen_filename() -> str:
    """Generates a filename from the current date."""
    return str(datetime.timestamp(datetime.now())).replace('.', '')


def shorten(s: str, approx_string_len: int = 10) -> str:
    """Shortens a string down to an amount of characters."""
    if len(s) < approx_string_len:
        return s

    return ' '.join(s[:approx_string_len + 1].split()[:-1]) + '...'


async def wait_for_reaction(ctx: Context, emoji: Emoji) -> bool:
    """Waiting for a user to react to a message sent by the bot."""

    def check(reaction, user: Context.author) -> bool:
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


class DefaultEmbed(Embed):
    """Subclassing the embed class to set defaults."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_footer(text=Config.BOT_DESCRIPTION, icon_url=Config.BOT_ICON_LINK)

        if 'embed_attachment' in kwargs.keys():
            v = kwargs['embed_attachment']
            f = v.split(os.sep)[-1]
            self.file = File(v, filename=f)

            self.set_image(url=f'attachment://{f}')

        elif 'single_url' in kwargs.keys():
            self.description = markdown_link(*kwargs['single_url'])

        elif 'description' in kwargs.keys():
            if '`' not in self.description and '\n' not in self.description:
                self.description = f'`{self.description}`'

        elif 'multiple_urls' in kwargs.keys():
            pass


async def check_if_blocked(ctx: Context, pool: asyncpg.pool.Pool) -> bool:
    """Checks if user/guild is blocked."""
    async with pool.acquire() as conn:
        # Check if user is blocked.
        _user = await conn.fetch(
            'SELECT * FROM Blocked_Users WHERE user_id = $1',
            ctx.author.id
        )

        if not len(_user):
            # If the user is not blocked, check if the guild is blocked.
            _guild = await conn.fetch(
                'SELECT * FROM Blocked_Guilds WHERE guild_id = $1',
                ctx.guild.id
            )
            if not len(_guild):
                return True

    # If none of the checks passed, either the guild or the user is blocked.
    return False


async def http_get(url: str, *, session: aiohttp.ClientSession) -> t.Any:
    """Small snippet to get json from a url."""
    async with session.get(url) as resp:
        assert resp.status == 200
        return await resp.json()
