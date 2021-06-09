import textwrap
import traceback

from discord.ext import commands
from discord.ext.commands import Cog
from loguru import logger as log

from xythrion import Context, Xythrion
from xythrion.utils import codeblock, markdown_link

BASE_URL = "https://api.duckduckgo.com/?q={}"


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

        search = ""
        title = "An error has occurred."

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
            title = "An unexpected error has occurred."

            trace = traceback.format_exception(type(e), e, e.__traceback__)

            log.error("".join(trace))

            trace = "\n".join(textwrap.wrap("".join(trace[-2:]).lstrip()))

            error_message = f"{type(e).__name__}: {e}"

            search = markdown_link("Search this error.", BASE_URL.format(error_message.replace(" ", "+")))

            return await ctx.embed(desc=f"**{title}**\n{codeblock(trace)}\n{search}")

        await ctx.embed(desc=f"**{title}**\n\n`{error_message}`")
