import os
from pathlib import Path

import qrcode
from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed, gen_filename


class QRCode(Cog):
    """Creating fractals out of user inputs."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @staticmethod
    def _create_qr_code(msg: str, fill_color: str, back_color: str) -> str:
        """Create the QR (quick response) code image."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(msg)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        f = Path.cwd() / 'tmp' / f'{gen_filename()}.png'
        img.save(f)
        return str(f)

    @command()
    async def qr(self, ctx: Context, msg: str, fill_color: str = 'black', back_color: str = 'white') -> None:
        """Giving a fractal to the user, with given inputs."""
        async with ctx.typing():
            f = await self.bot.loop.run_in_executor(None, self._create_qr_code, msg, fill_color, back_color)

        embed = DefaultEmbed(ctx, embed_attachment=f)

        await ctx.send(file=embed.file, embed=embed)

        os.remove(f)
