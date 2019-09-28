"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * More interactions to come in the future.
"""


from discord.ext import commands as comms
import discord

from modules.output import ds


class Interactions_Director(comms.Cog):
    """Special interactions between the bot and users"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.Cog.listener()
    async def on_guild_remove(self, guild):
        ds.s(f'Bot has left guild {guild}')

    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        ds.s(f'Bot has joined guild {guild}')


def setup(bot):
    bot.add_cog(Interactions_Director(bot))
