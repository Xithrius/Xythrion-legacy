"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Messages(comms.Cog):
    """"""

    def __init__(self, bot):
        self.bot = bot

    @comms.command(enabled=False)
    async def remove_messages(self, ctx, amount: int=None):
        messages = await channel.history(limit=amount).flatten()


def setup(bot):
    bot.add_cog(Messages(bot))