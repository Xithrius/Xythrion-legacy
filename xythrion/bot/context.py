from datetime import datetime
from io import BytesIO
from typing import Optional

from disnake import Embed, File
from disnake.ext import commands
from humanize import naturaldelta


class Context(commands.Context):
    """Custom methods for Context that the base doesn't provide."""

    async def send(self, *args, **kwargs) -> None:
        """
        The same as the regular send function, but returns nothing.

        This is useful for having a return statement along with a send function on the same line.
        """
        await super().send(*args, **kwargs)

    async def check_for_subcommands(self) -> None:
        """If an invalid subcommand is passed, this is brought up."""
        if self.invoked_subcommand is None:
            command_list = ", ".join(x.name for x in self.bot.commands if x.enabled)

            await self.embed(desc=f"Unknown command. Available group command(s): {command_list}")

    async def embed(
            self,
            *,
            desc: Optional[str] = None,
            buffer: Optional[BytesIO] = None,
            image_url: Optional[str] = None
    ) -> None:
        """Creating then sending embeds."""
        startup_delta = naturaldelta(datetime.now() - self.bot.startup_time)

        embed = Embed()

        if desc:
            if any(x in desc for x in ['\n', '`']):
                embed.description = f'`{desc}`'
            else:
                embed.description = desc

        embed.set_footer(text=f"Bot uptime: {startup_delta}.")

        if buffer:
            embed.set_image(url="attachment://temporary_image_file.png")

            file = File(fp=buffer, filename="temporary_image_file.png")

            return await self.send(embed=embed, file=file)

        elif image_url:
            embed.set_image(url=image_url)

        await self.send(embed=embed)
