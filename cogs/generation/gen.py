"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import os

import qrcode
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord

from modules import gen_filename, path


class Gen(comms.Cog):
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

    def create_qr_code(self, msg: str):
        # img = qrcode.make(msg)
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

    @comms.cooldown(1, 10, BucketType.user)
    @comms.command()
    async def qr(self, ctx, *, msg: str):
        lock = asyncio.Lock()

        async with lock:
            f = await self.bot.loop.run_in_executor(None, self.create_qr_code, msg)
            file = discord.File(path('tmp', f), filename=f)

        await ctx.send(file=file)
        os.remove(path('tmp', f))


def setup(bot):
    bot.add_cog(Gen(bot))
