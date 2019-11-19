"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import random
import datetime

from discord.ext import commands as comms
import discord

from modules.shortcuts import embed


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
        await ctx.send(
            f'{user.mention} has sent {len(messages)} in {ctx.channel}')

    @comms.command()
    async def stackoverflow(self, ctx, year: int):
        """ """
        if 2019 >= year >= 2015:
            await ctx.send(f'https://insights.stackoverflow.com/survey/{year}')
        else:
            raise comms.UserInputError('Year must be between 2019 and 2015')

    @comms.command()
    async def runtime(self, ctx):
        async with self.bot.pool.acquire() as conn:
            t = await conn.fetch(
                '''SELECT avg(logout - login) avg_uptime,
                          max(logout - login) max_uptime FROM Runtime''')

        avg = str((datetime.datetime.min + t[0]['avg_uptime']).time()).split(':')
        _max = str((datetime.datetime.min + t[0]['max_uptime']).time()).split(':')

        timestamps = ['Hours', 'Minutes', 'Seconds']
        avg_str = ', '.join(
            f'{int(float(avg[i]))} {timestamps[i]}' for i in range(len(
                timestamps)) if float(avg[i]) != 0.0)
        max_str = ', '.join(
            f'{int(float(_max[i]))} {timestamps[i]}' for i in range(len(
                timestamps)) if float(_max[i]) != 0.0)
        
        login_time = self.bot.login_time.strftime(
            '%A %I:%M:%S%p'
            ).lower().capitalize().replace(" ", " at ")

        desc = [
            f'Login time was `{login_time}`',
            f'Average uptime is `{avg_str}`',
            f'Longest uptime was `{max_str}`'
        ]
        e = embed(title='Bot runtime information',
                  desc=desc)
        await ctx.send(embed=e)
        

def setup(bot):
    bot.add_cog(Misc_Director(bot))
