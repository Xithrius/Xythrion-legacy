"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import random
import datetime
import numpy

from discord.ext import commands as comms
import discord

from modules.output import now


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
    async def stackoverflow(self, ctx, year: int):
        """ """
        if 2019 >= year >= 2015:
            await ctx.send(f'https://insights.stackoverflow.com/survey/{year}')
        else:
            raise comms.UserInputError('Year must be between 2019 and 2015')

    @comms.command()
    async def uptime(self, ctx):
        running_time = datetime.datetime.now() - self.bot.login_time
        delta = str((datetime.datetime.min + running_time).time()).split(':')
        timestamps = ['Hours', 'Minutes', 'Seconds']
        running_time_delta = ', '.join(f'{int(float(delta[i]))} {timestamps[i]}' for i in range(len(timestamps)) if float(delta[i]) != 0.0)
        times = await self.bot.conn.fetch('''SELECT login, logout FROM Runtime''')
        a_u = [str((datetime.datetime.min + (t['logout'] - t['login'])).time()).split(':') for t in times]
        a_u = numpy.array([[float(y) for y in x] for x in a_u])
        a_u = [round(sum(a_u[:,x]) / len(times), 1) for x in range(3)]
        embed = discord.Embed(title=f"Running since {self.bot.login_time.strftime('%A %I:%M:%S%p').lower().capitalize()}; Total uptime {running_time_delta}",
                              description=f'Average uptime: {", ".join(f"{a_u[i]} {timestamps[i]}" for i in range(len(a_u)) if a_u[i] != 0)}\nTotal logins: {len(times)}', 
                              timestamp=now(), colour=self.bot.ec)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc_Director(bot))
