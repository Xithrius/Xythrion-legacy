import logging

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
    async def on_command_error(self, ctx: Context, error: commands.CommandError) -> None:
        """When the command has an error, this event is triggered."""
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        await ctx.message.add_reaction('\U0000274c')

        embed = DefaultEmbed(ctx, title='**An error has occurred:**')

        if isinstance(error, commands.DisabledCommand):
            embed.description = 'Command not available.'

        elif isinstance(error, commands.UserInputError):
            embed.description = f'Command raised bad argument: {error}.'

        elif isinstance(error, commands.NotOwner):
            embed.description = 'You do not have enough permissions for this command.'

        elif isinstance(error, commands.CommandOnCooldown):
            embed.description = f'{error}.'

        elif isinstance(error, commands.CheckFailure):
            embed.description = 'You do not have enough permissions to run this command.'

        elif isinstance(error, commands.MissingPermissions):
            embed.description = 'Bot does not have enough permissions for this command.'

        elif isinstance(error, commands.CommandNotFound):
            embed.description = 'Unknown command.'

        else:
            embed.description = f'{type(error).__name__}: {error}'

        embed.description = f'`{embed.description}`'

        await ctx.send(embed=embed)

        log.info(f'{type(error).__name__}: {error}')
