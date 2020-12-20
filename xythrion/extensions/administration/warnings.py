import logging

from discord.ext import commands
from discord.ext.commands import Cog, Context

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed

log = logging.getLogger(__name__)


class Warnings(Cog, command_attrs=dict(hidden=True)):
    """Warning the user about specific actions taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: Context) -> None:
        """Adds a reaction after a command is successfully completed."""
        await ctx.message.add_reaction("\U00002705")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, e: commands.CommandError) -> None:
        """When the command has an error, this event is triggered."""
        if hasattr(ctx.command, "on_error"):
            return

        e = getattr(e, "original", e)

        await ctx.message.add_reaction("\U0000274c")

        embed = DefaultEmbed(ctx, title="**An error has occurred:**")

        if isinstance(e, commands.DisabledCommand):
            embed.description = "Command not currently enabled."

        elif isinstance(e, commands.UserInputError):
            embed.description = f"Command received bad argument: {e}."

        elif isinstance(e, commands.NotOwner):
            embed.description = "You do not have enough permissions for this command."

        elif isinstance(e, commands.CommandOnCooldown):
            embed.description = f"{e}."

        elif isinstance(e, commands.CheckFailure):
            embed.description = "You do not have enough permissions to run this command."

        elif isinstance(e, commands.MissingPermissions):
            embed.description = "Bot does not have enough permissions for this command."

        elif isinstance(e, commands.CommandNotFound):
            embed.description = "Unknown command."

        else:
            embed.description = f"{type(e).__name__}: {e}"

        log.error("An error has occurred.", exc_info=(type(e), e, e.__traceback__))

        embed.description = f"`{embed.description}`"

        await ctx.send(embed=embed)
