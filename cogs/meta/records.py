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
        ctx = await self.bot.get_context(message)
        is_message = ctx.valid
        if is_message:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO Messages(t, id, jump) VALUES ($1, $2, $3)''',
                    message.created_at, message.author.id, message.jump_url
                )

    @comms.Cog.listener()
    async def on_command(self, ctx):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Commands(t, id, jump, command) VALUES ($1, $2, $3, $4)''',
                datetime.datetime.now(), ctx.author.id, ctx.message.jump_url, str(ctx.command)
            )

    @comms.Cog.listener()
    async def on_command_completion(self, ctx):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''UPDATE Commands SET completed=$2 WHERE jump=$1''',
                ctx.message.jump_url, datetime.datetime.now()
            )

    @comms.command(enabled=False)
    async def rank(self, ctx, user: discord.User = None):
        """Gets rank information about the user.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (discord.User): The user that will have their information retrieved (defaulted to None).

        """
        user = user.id if user is not None else ctx.author.id

    @comms.command()
    async def uptime(self, ctx):
        """Gives uptime information about the bot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        async with self.bot.pool.acquire() as conn:
            t = await conn.fetch(
                '''SELECT avg(t_logout - t_login) avg_uptime,
                          max(t_logout - t_login) max_uptime,
                          min(t_logout - t_login) min_uptime FROM Runtime''')
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
