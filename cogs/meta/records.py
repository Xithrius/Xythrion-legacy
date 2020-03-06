"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord


class Records(comms.Cog):
    """Recording and outputting information based on users, by users.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.Cog.listener()
    async def on_message(self, message):
        """Records every single message sent by users for ranking.
        
        Args:
            message (discord.Message): Represents a message from Discord 

        """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Messages(identification, message_date) VALUES ($1, $2)''',
                message.author.id, datetime.datetime.now())

    @comms.command()
    @comms.cooldown(1, 5, BucketType.user)
    async def rank(self, ctx, user: discord.User = None):
        """Gets rank information about the user.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (discord.User): The user that will have their information retrieved (defaulted to None).

        """
        user = user if user is not None else ctx.author
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT message_date from Messages WHERE identification=$1''',
                user.id)
            embed = discord.Embed(title=f'Calculated rank for "{user.name}":',
                                description=f'`{len(info)} messages sent.`')
            await ctx.send(embed=embed)

    @comms.command()
    @comms.cooldown(1, 5, BucketType.user)
    async def uptime(self, ctx):
        """Gives uptime information about the bot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        async with self.bot.pool.acquire() as conn:
            t = await conn.fetch(
                '''SELECT avg(logout - login) avg_uptime,
                          max(logout - login) max_uptime,
                          min(logout - login) min_uptime FROM Runtime''')
            t = dict(t[0])

        timestamps = ['Hours', 'Minutes', 'Seconds']
        
        for k, v in t.items():
            # datetime.timedelta to formatted datetime.datetime
            tmp = str((datetime.datetime.min + v).time()).split(':')
            t[k] = ', '.join(f'{int(float(tmp[i]))} {timestamps[i]}' for i in range(len(timestamps)) if float(tmp[i]) != 0.0)

        # Inserting the login time for the bot.
        login = self.bot.startup_time.strftime('%A %I:%M:%S%p').lower().capitalize().replace(" ", " at ")
        t = {'login_time': login, **t}
        
        # Putting everything together for formatting.
        lst = [f'Login time', f'Average uptime', f'Longest uptime', f'Shortest uptime' ]
        lst = [f'{y[0]}: {y[1]}' for y in zip(lst, t.values())]
        lst = '\n'.join(str(y) for y in lst)
        
        embed = discord.Embed(title='*Bot uptime information:*', description=f'```py\n{lst}\n```')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Records(bot))
