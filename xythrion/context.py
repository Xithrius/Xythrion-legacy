from datetime import datetime
from io import BytesIO
from typing import Optional

from discord import Embed, File
from discord.ext import commands
from humanize import naturaldelta


class Context(commands.Context):
    """Customization of methods for context."""

    async def send(self, *args, **kwargs) -> None:
        """
        The same as the regular send function, but returns nothing.

        This is useful for having a return statement along with a send function on the same line.
        """
        await super().send(*args, **kwargs)

    async def check_for_subcommands(self) -> None:
        """If an invalid subcommand is passed, this is brought up."""
        if self.invoked_subcommand is None:
            lst = ", ".join(x.name for x in self.command.commands if x.enabled)

            error_string = f"Unknown command. Available group command(s): {lst}"

            await self.embed(desc=error_string)

    async def embed(
            self,
            *,
            desc: Optional[str] = None,
            buffer: Optional[BytesIO] = None,
            image_url: Optional[str] = None
    ) -> Optional[Embed]:
        """Creating then sending embeds."""
        startup_delta = naturaldelta(datetime.now() - self.bot.startup_time)

        description = f'`{desc}`' if '\n' not in desc else desc

        embed = Embed(description=description)

        embed.set_footer(text=f"Bot uptime: {startup_delta}.")

        if buffer:
            embed.set_image(url="attachment://temporary_image_file.png")

            buffer.seek(0)

            file = File(fp=buffer.read(), filename="temporary_image_file.png")

            return await self.send(embed=embed, file=file)

        elif image_url:
            embed.set_image(url=image_url)

        await self.send(embed=embed)
