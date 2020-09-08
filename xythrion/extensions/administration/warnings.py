import logging
from typing import Optional

from discord import Message
from discord.ext import commands
from discord.ext.commands import Cog, Context
from fuzzywuzzy import process

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

        elif isinstance(error, commands.CommandNotFound):
            # Tries to suggest similar commands.
            _cmd = ctx.message.content[len(ctx.prefix):].split()[0]
            query = process.extract(_cmd, [x for x in self.bot.commands if not x.hidden])
            found = '\n'.join(f'`{ctx.prefix}{x[0].name}`' for x in query) if len(query) else None
            embed = DefaultEmbed(description=found)

            embed.title = f'Command "{_cmd}" not found.{" Suggestions:" if found else ""}'

            return await ctx.send(embed=embed)

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

        else:
            log.critical(f'Error occurred: {error}')

            await ctx.send(f'`An error has occurred: {type(error)} {error} {error.args}`')
