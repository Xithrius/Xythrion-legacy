"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from pathlib import Path

from discord.ext.commands import Cog, command, Context
import qrcode
from xythrion.bot import Xythrion
from xythrion.utils import gen_filename, parallel_executor


class QRCode(Cog):
    """Creating fractals out of user inputs."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @parallel_executor
    def create_qr_code(self, msg: str) -> str:
        """Create the QR (quick response) code image."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(msg)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')

        f = f'{gen_filename()}.png'
        img.save(Path.cwd() / 'tmp' / f)
        return f

    @command()
    async def qr(self, ctx: Context) -> None:
        """Giving a fractal to the user, with given inputs."""
        pass
