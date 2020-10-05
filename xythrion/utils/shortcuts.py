import asyncio
import os
import typing as t
from datetime import datetime

import aiohttp
from discord import Embed, Emoji, File, Member, Message, Reaction, TextChannel
from discord.ext.commands import BadArgument, Context, MessageConverter
from humanize import naturaldelta


def gen_filename() -> str:
    """Generates a filename from the current date."""
    return str(datetime.timestamp(datetime.now())).replace('.', '')


def shorten(s: t.Union[t.List[str], str], min_chars: int = 100, max_chars: int = 2000
            ) -> t.Union[t.List[str], str]:
    """Shortens a string down to an amount of characters."""
    if isinstance(s, str):
        return ' '.join(s[:min_chars + 1].split()[:-1]) + '...' if len(s) > min_chars else s

    elif isinstance(s, list):
        return [lst for index, lst in enumerate(s) if sum(map(len, s[:index])) < max_chars]

    else:
        raise ValueError('This function only accepts strings or a list of lists with strings.')


async def wait_for_reaction(ctx: Context, emoji: Emoji) -> bool:
    """Waiting for a user to react to a message sent by the bot."""

    def check(reaction: Reaction, user: Context.author) -> bool:
        return user == ctx.message.author and str(reaction.emoji) == emoji

    try:
        _, __ = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

    except asyncio.TimeoutError:
        pass

    else:
        return True


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


async def check_for_subcommands(ctx: Context) -> None:
    """If an invalid subcommand is passed, this is brought up."""
    lst = ', '.join([x.name for x in ctx.command.commands if x.enabled])

    error_string = f'Unknown command. Available group command(s): {lst}'

    embed = DefaultEmbed(ctx, description=error_string)

    await ctx.send(embed=embed)


async def http_get(url: str, *, session: aiohttp.ClientSession) -> t.Any:
    """Small snippet to get json from a url."""
    async with session.get(url) as resp:
        assert resp.status == 200, resp.raise_for_status()
        return await resp.json()


class DefaultEmbed(Embed):
    """Subclassing the embed class to set defaults."""

    def __init__(self, ctx: Context, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_footer(text=f'Bot uptime: {naturaldelta(datetime.now() - ctx.bot.startup_time)}.')

        if 'embed_attachment' in kwargs.keys():
            v = kwargs['embed_attachment']
            f = str(v).split(os.sep)[-1]
            self.file = File(v, filename=f)

            self.set_image(url=f'attachment://{f}')

        elif 'description' in kwargs.keys():
            if '`' not in self.description and '\n' not in self.description:
                self.description = f'`{self.description}`'
