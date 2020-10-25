"""Command to get a link to the source repo for this project."""
import inspect

from pathlib import Path
from typing import Optional, Tuple, Union

from discord import Colour, Embed
from discord.ext import commands

from xythrion.constants import Config

GITHUB_URL = Config.GITHUB_URL

SourceType = Union[
    commands.HelpCommand,
    commands.Command,
    commands.Cog,
    str,
    commands.ExtensionNotLoaded,
]


class SourceConverter(commands.Converter):
    """Convert an argument into a help command, tag, command, or cog."""

    # special thanks to Pydis
    async def convert(self, ctx: commands.Context, argument: str) -> SourceType:
        """Convert argument into source object."""
        if argument.lower().startswith("help"):
            return ctx.bot.help_command

        cog = ctx.bot.get_cog(argument)
        if cog:
            return cog

        cmd = ctx.bot.get_command(argument)
        if cmd:
            return cmd

        tags_cog = ctx.bot.get_cog("Tags")
        show_tag = True

        if not tags_cog:
            show_tag = False
        elif argument.lower() in tags_cog._cache:
            return argument.lower()

        raise commands.BadArgument(
            f"Unable to convert '{argument}' to valid command{', tag,' if show_tag else ''} or Cog."
        )

    @staticmethod
    def get_source_location(src_obj: SourceType) -> Tuple[str, str, Optional[int]]:
        """Attemps to get the source of a command and build the URL."""
        if isinstance(src_obj, commands.Command):
            src = src_obj.callback.__code__
            filename = src.co_filename
        else:
            src = type(src_obj)

            try:
                filename = inspect.getsourcefile(src)
            except TypeError:
                raise commands.BadArgument("Cannot get source for a dynamically-created object.")

        if not isinstance(src_obj, str):
            try:
                lines, first_line_no = inspect.getsourcelines(src)
            except OSError:
                raise commands.BadArgument("Cannot get source for a dynamically-created object.")

            lines_extension = f"#L{first_line_no}-L{first_line_no + len(lines) - 1}"
        else:
            first_line_no = None
            lines_extension = ""

        file_location = Path(filename).relative_to(Path.cwd()).as_posix()

        url = f"{GITHUB_URL}/blob/master/{file_location}{lines_extension}"

        return url, file_location, first_line_no or None


class Source(commands.Cog):
    """Command to send the source (github repo) of a command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="source", brief="Send a link to Xythrion's GitHub repo")
    async def send_source(self, ctx: commands.Context, arg1: str = "") -> None:
        """Send the source GitGub url in an embed."""
        src_conv = SourceConverter()
        if arg1:
            try:
                src_obj = await src_conv.convert(ctx, arg1)
                src_url = src_conv.get_source_location(src_obj)[0]

                if hasattr(src_obj, 'brief'):
                    desc = f"Description: {src_obj.brief}"
                else:
                    desc = "Extension"

                embed = Embed(
                    title="Xythrion's GitHub Repo",
                    colour=Colour.blue(),
                    description=desc,
                )
                embed.add_field(
                    name="Repository",
                    value=f"[Go To GitHub]({src_url})",
                )
                await ctx.send(embed=embed)
            except commands.BadArgument as e:
                raise e
        else:
            embed = Embed(title="Xythrion's GitHub Repo", colour=Colour.blue())
            embed.add_field(
                name="Repository", value=f"[Go To GitHub]({GITHUB_URL})"
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the Source cog."""
    bot.add_cog(Source(bot))
