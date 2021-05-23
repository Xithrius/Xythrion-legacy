from discord.ext import commands
from discord.ext.commands import Cog
from loguru import logger as log

from xythrion import Context, Xythrion


class Warnings(Cog, command_attrs=dict(hidden=True)):
    """Warning a user about the actions that they've taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, e: commands.CommandError) -> None:
        """When a command has an error, this event is triggered."""
        if hasattr(ctx.command, "on_error"):
            return

        e = getattr(e, "original", e)

        title = "**An error has occurred:**\n\n"

        if isinstance(e, commands.DisabledCommand):
            error_message = "Command not currently enabled."

        elif isinstance(e, commands.UserInputError):
            error_message = f"Command received bad argument: {e}."

        elif isinstance(e, commands.NotOwner):
            error_message = "You do not have enough permissions for this command."

        elif isinstance(e, commands.CommandOnCooldown):
            error_message = f"{e}."

        elif isinstance(e, commands.CheckFailure):
            error_message = "You do not have enough permissions to run this command."

        elif isinstance(e, commands.MissingPermissions):
            error_message = "Bot does not have enough permissions for this command."

        elif isinstance(e, commands.CommandNotFound):
            error_message = "Unknown command."

        else:
            error_message = f"{type(e).__name__}: {e}"

            log.error("An error has occurred.", exc_info=(type(e), e, e.__traceback__))

        await ctx.embed(desc=f"{title}\n\n{error_message}")
