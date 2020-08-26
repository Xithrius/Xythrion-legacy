"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from datetime import datetime
from logging import getLogger
from typing import Optional

from discord import Embed
from discord.ext.commands import Cog, command, Context, ExtensionNotLoaded, Greedy
import humanize
from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS

log = getLogger(__name__)


class Development(Cog):
    """Cog required for development and control."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is the owner of this bot."""
        return await self.bot.is_owner(ctx.author)

    @command(name='reload', aliases=('refresh', 'r'), hidden=True)
    async def _reload(self, ctx: Context, ext: Optional[str] = None) -> None:
        """Reloads all extensions."""
        d = datetime.now()

        for extension in EXTENSIONS:
            try:
                self.bot.reload_extension(extension)

            except ExtensionNotLoaded:
                self.bot.load_extension(extension)

            except Exception as e:
                return log.warning(f'Reloading {extension} error: {e}')

        log.info((
            f'{ctx.author.name} reloaded extension{"" if ext else "s"} successfully. '
            f'In about {humanize.naturaldelta(d - datetime.now(), minimum_unit="milliseconds")}ms'
        ))

        await ctx.send(f'`Extension{" " + ext if ext else "s"} reloaded.`')

    @command(name='logout', hidden=True)
    async def _logout(self, ctx: Context) -> None:
        """Makes the bot Log out."""
        await ctx.bot.logout()

    @command(name='loaded', hidden=True)
    async def _loaded_extensions(self, ctx: Context) -> None:
        """Gives a list of the currently loaded cogs."""
        extensions = '\n'.join(f'{str(i).zfill(3)} | {ext}' for i, ext in enumerate(self.bot.cogs))

        embed = Embed(title='*Currently loaded cogs:*', description=f'```py\n{extensions}\n```')

        await ctx.send(embed=embed)

    @command(name='echo', aliases=('say',))
    async def _echo(self, ctx: Context, channel_id: Greedy[int], *, msg: str) -> None:
        """Makes the bot send a message to a channel."""
        channel = self.bot.get_channel(channel_id[0]) if channel_id else ctx.channel
        await channel.send(msg)

    @command(name='embed')
    async def _embed(self, ctx: Context, *, desc: Optional[str] = None) -> None:
        """Testing out embed descriptions. Discord markdown supported, obviously."""
        embed = Embed(description=desc if desc else '')
        await ctx.send(embed=embed)

    @command(name='raw')
    async def _raw(self, ctx: Context, msg: str) -> None:
        pass
