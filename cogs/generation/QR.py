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

from modules import embed_attachment, gen_filename, lock_executor, path, ast


class QR(comms.Cog):
    """Summary for Gen

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific functions """

    def create_qr_code(self, msg: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(msg)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        f = f'{gen_filename()}.png'
        img.save(path('tmp', f))
        return f

    """ Commands """

    @comms.cooldown(1, 10, BucketType.user)
    @comms.command()
    async def qr(self, ctx, *, msg: str):
        """Generates a Quick Response code for a string.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            msg (str): The message to be converted into a QR code.

        Command examples:
            >>> [prefix]something
            >>> [prefix]another thing

        """
        f = await lock_executor(self.create_qr_code, [msg], loop=self.bot.loop)
        embed = discord.Embed(title=ast(f'QR code for "{msg}":'))
        file, embed = embed_attachment(path('tmp', f), embed)

        await ctx.send(file=file, embed=embed)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(QR(bot))
