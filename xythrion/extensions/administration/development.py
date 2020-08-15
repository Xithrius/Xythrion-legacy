"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime
from logging import getLogger
from typing import Optional

import discord
import humanize
from discord.ext import commands as comms
from discord.ext.commands import Cog, Context

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import markdown_link


log = getLogger(__name__)


class Development(Cog):
    """Cog required for development and control"""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @comms.command(name='reload', aliases=['refresh', 'r'], hidden=True)
    @comms.is_owner()
    async def _reload(self, ctx: Context, ext: Optional[str] = None) -> None:
        """Reloads all extensions within the `EXTENSION` variable."""
        d = datetime.now()

        for extension in await EXTENSIONS:
            try:
                self.bot.reload_extension(extension)

            except comms.ExtensionNotLoaded:
                self.bot.load_extension(extension)

            except Exception as e:
                return log.warning(f'Reloading {extension} error: {e}')

        log.info((
            "Reloaded extensions in about"
            f"{humanize.naturaldelta(d - datetime.now(), minimum_unit='milliseconds')}"
        ))

    @comms.command(name='logout', hidden=True)
    @comms.is_owner()
    async def _logout(self, ctx: Context) -> None:
        """Makes the bot Log out."""
        await self.bot.logout()

    @comms.command(name='loaded', hidden=True)
    @comms.is_owner()
    async def _loaded_extensions(self, ctx: Context) -> None:
        """Gives a list of the currently loaded cogs."""
        lst = [f'{str(i).zfill(3)} | {ext}' for i, ext in enumerate(EXTENSIONS)]
        c = '\n'.join(str(y) for y in lst)

        embed = discord.Embed(title='*Currently loaded cogs:*', description=f'```py\n{c}\n```')

        await ctx.send(embed=embed)

    @comms.command(name='help', aliases=['h'])
    async def _help(self, ctx: Context) -> None:
        """Giving help to a user."""
        lst = [
            '`Help is most likely not ready yet, check the link just in case:`',
            markdown_link('Help with commands link', 'https://github.com/Xithrius/Xythrion#commands')
        ]

        embed = discord.Embed(description='\n'.join(map(str, lst)))

        await ctx.send(embed=embed)

    @comms.command(name='issue', aliases=['problem', 'issues'])
    async def _issue(self, ctx: Context) -> None:
        """Gives the user the place to report issues."""
        url = 'https://github.com/Xithrius/Xythrion/issues'
        embed = discord.Embed(description=markdown_link('Report issue(s) here', url))

        await ctx.send(embed=embed)
