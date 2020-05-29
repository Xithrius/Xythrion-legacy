"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os

import discord
import qrcode
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from utils import (
    embed_attachment, get_filename, path, parallel_executor
)


class QR(comms.Cog):
    """Summary for Gen

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot) -> None:
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific functions """

    @parallel_executor
    def create_qr_code(self, msg: str) -> str:
        """Creating the QR code image.

        Args:
            msg (str): The message to be converted to binary.

        Returns:
            str: The path of the image.

        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        qr.add_data(msg)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        f = f'{get_filename()}.png'

        img.save(path('tmp', f))

        return f

    """ Commands """

    @comms.cooldown(1, 10, BucketType.user)
    @comms.command()
    async def qr(self, ctx: comms.Context, *, msg: str) -> None:
        """Generates a Quick Response code for a string.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            msg (str): The message to be converted into a QR code.

        Returns:
            bool: Always None.

        Command examples:
            >>> [prefix]something
            >>> [prefix]another thing

        """
        f = await self.create_qr_code([msg])

        embed = discord.Embed()
        file, embed = embed_attachment(path('tmp', f), embed)

        embed.description = f'`{bin(msg)[2:]}`'

        await ctx.send(file=file, embed=embed)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(QR(bot))
