import logging
from typing import Optional

from discord import Message
from discord.ext import commands
from discord.ext.commands import Cog, Context

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

log = logging.getLogger(__name__)


class Warnings(Cog):
    """Warning the user about specific actions taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: Context) -> None:
        """Adds a reaction after a command is successfully completed."""
        await ctx.message.add_reaction('\U00002705')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError) -> Optional[Message]:
        """When the command has an error, this event is triggered."""
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        await ctx.message.add_reaction('\U0000274c')

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send('`Command not available.`')

        elif isinstance(error, commands.UserInputError):
            return await ctx.send(f'`Command raised bad argument: {error}`')

        elif isinstance(error, commands.NotOwner):
            return await ctx.send('`You do not have enough permissions for this command.`')

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'`{error}`')

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send('`You do not have enough permissions to run this command.`')

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send('`Bot does not have enough permissions for this command.`')

        embed = DefaultEmbed(ctx, title='**An error has occurred:**',
                             description=f'{type(error).__name__}: {error}')

        await ctx.send(embed=embed)

        log.warning(f'Error: {type(error).__name__}: {error}')
