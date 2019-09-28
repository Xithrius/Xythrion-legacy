"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import random

from discord.ext import commands as comms
import discord

from modules.output import ds


class Misc_Director(comms.Cog):
    """ """

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command()
    async def get_icon(self, ctx, user: discord.User):
        await ctx.send(user.avatar_url)

    @comms.command()
    async def roll(self, ctx, bottom: int, top: int):
        if not any([isinstance(x, int) for x in [bottom, top]]):
            raise ValueError
        else:
            await ctx.send(random.randint(bottom, top + 1))

    @comms.command()
    async def flip(self, ctx):
        await ctx.send(random.choice(['heads', 'tails']))

    @comms.command(name='choice')
    async def _choice(self, ctx, *args):
        await ctx.send(random.choice(args))

    @comms.command()
    async def count_messages(self, ctx, user: discord.User, limit=None):
        async with ctx.typing():
            messages = await ctx.channel.history(limit=limit).flatten()
            messages = [x for x in messages if x.author.id == user.id]
        await ctx.send(f'{user.mention} has sent {len(messages)} in {ctx.channel}')

    @comms.command()
    async def scan_messages(self, ctx, item, limit=None):
        messages = await ctx.channel.history(limit=limit).flatten()
        messages = [x for x in messages if x.author.id == ctx.author.id and item in x.message.content]


def setup(bot):
    bot.add_cog(Misc_Director(bot))
