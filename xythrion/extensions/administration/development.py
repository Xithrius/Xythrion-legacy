from datetime import datetime
from logging import getLogger
from typing import Optional

import humanize
from discord import Embed, Message
from discord.ext.commands import Cog, Context, ExtensionNotLoaded, Greedy, command
from tabulate import tabulate

from xythrion.bot import Xythrion
from xythrion.extensions import EXTENSIONS
from xythrion.utils import DefaultEmbed

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

        ms = humanize.naturaldelta(d - datetime.now(), minimum_unit="milliseconds")

        log.info(
            f'{ctx.author.name} reloaded extension{"" if ext else "s"} successfully in about {ms}.'
        )

        await ctx.send(f'`Extension{" " + ext if ext else "s"} reloaded in about {ms}`')

    @command(name='logout', hidden=True)
    async def _logout(self, ctx: Context) -> None:
        """Makes the bot Log out."""
        await ctx.bot.logout()

    @command(name='loaded', hidden=True)
    async def _loaded_extensions(self, ctx: Context) -> None:
        """Gives a list of the currently loaded cogs."""
        extensions = '\n'.join(f'{str(i).zfill(3)} | {ext}' for i, ext in enumerate(self.bot.cogs))

        embed = Embed(title='*Currently loaded cogs:*', description=f'```py\n{extensions}\n```')

        embed = DefaultEmbed(description=f'```py\n{extensions}\n```')

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
        """All information from a message object, if one can be found."""
        pass

    @command(name='sql')
    async def _sql(self, ctx: Context, command_type: str, *, _command: str) -> Optional[Message]:
        """Executes a command given by the user. User has to be an owner."""
        async with self.bot.pool.acquire() as conn:
            if command_type == 'fetch':
                output = await conn.fetch(_command)

                keys = list(output[0].keys())
                table = tabulate([[x[k] for k in keys] for x in output], showindex='Always', headers=keys)

                await ctx.send(f'```sql\n{table}```')

            elif command_type == 'execute':
                output = await conn.execute(_command)
                await ctx.send(f'```sql\n{output}```')

            else:
                embed = DefaultEmbed(description=f'"{command_type}" is not a valid command type.')
                return await ctx.send(embed=embed)
