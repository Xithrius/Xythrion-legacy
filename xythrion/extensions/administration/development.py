from datetime import datetime
from logging import getLogger
from typing import Optional

import humanize
from discord import Embed
from discord.ext.commands import Cog, Context, ExtensionNotLoaded, command

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import DefaultEmbed

log = getLogger(__name__)


class Development(Cog, command_attrs=dict(hidden=True)):
    """Cog required for development and control."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is the owner of this bot."""
        return await self.bot.is_owner(ctx.author)

    @command(name='reload', aliases=('refresh', 'r'))
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

        ms = humanize.naturaldelta(d - datetime.now(), minimum_unit="milliseconds")

        log.info(
            f'{ctx.author.name} reloaded extension{"" if ext else "s"} successfully in about {ms}.'
        )

        await ctx.send(f'`Extension{" " + ext if ext else "s"} reloaded in about {ms}`')

    @command(name='logout')
    async def _logout(self, ctx: Context) -> None:
        """Makes the bot Log out."""
        await ctx.bot.logout()

    @command(name='loaded')
    async def _loaded_extensions(self, ctx: Context) -> None:
        """Gives a list of the currently loaded cogs."""
        extensions = '\n'.join(f'{str(i).zfill(3)} | {ext}' for i, ext in enumerate(self.bot.cogs))

        embed = Embed(title='*Currently loaded cogs:*', description=f'```py\n{extensions}\n```')

        embed = DefaultEmbed(description=f'```py\n{extensions}\n```')

        await ctx.send(embed=embed)

    @command(name='embed')
    async def _embed(self, ctx: Context, *, desc: Optional[str] = None) -> None:
        """Testing out embed descriptions. Discord markdown supported, obviously."""
        embed = Embed(description=desc if desc else '')
        await ctx.send(embed=embed)
