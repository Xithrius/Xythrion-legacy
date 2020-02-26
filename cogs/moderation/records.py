"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Records(comms.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot

    @comms.Cog.listener()
    async def on_message(self, message):
        """ """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Messages(identification, message_date) VALUES ($1, $2)''',
                message.author.id, datetime.datetime.now())


    # async def rank(self, ctx, user_id: int = ):
    @comms.command(enabled=False)
    async def rank(self, ctx, user_id):
        """ """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT message_date from Messages WHERE identification=$1''',
                ctx.author.id)
            return await ctx.send(len(info))

    @comms.command()
    async def uptime(self, ctx):
        """ """
        async with self.bot.pool.acquire() as conn:
            t = await conn.fetch(
                '''SELECT avg(logout - login) avg_uptime,
                          max(logout - login) max_uptime FROM Runtime''')

        avg = str((datetime.datetime.min + t[0]['avg_uptime']).time()).split(':')
        _max = str((datetime.datetime.min + t[0]['max_uptime']).time()).split(':')

        timestamps = ['Hours', 'Minutes', 'Seconds']
        avg_str = ', '.join(f'{int(float(avg[i]))} {timestamps[i]}' for i in range(len(timestamps)) if float(avg[i]) != 0.0)
        max_str = ', '.join(f'{int(float(_max[i]))} {timestamps[i]}' for i in range(len(timestamps)) if float(_max[i]) != 0.0)
        
        login_time = self.bot.startup_time.strftime('%A %I:%M:%S%p').lower().capitalize().replace(" ", " at ")

        lst = [
            f'Login time was `{login_time}`',
            f'Average uptime is `{avg_str}`',
            f'Longest uptime was `{max_str}`'
        ]
        embed = discord.Embed(title=f'*Bot runtime information:*',
                              description='\n'.join(y for y in lst))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Records(bot))
