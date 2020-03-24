"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import discord
from discord.ext import commands as comms

from modules import gen_block


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
            message (discord.Message): Represents a message from Discord.

        """
        ctx = await self.bot.get_context(message)
        if not ctx.valid:
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
                datetime.now(), ctx.author.id, ctx.message.jump_url, str(ctx.command)
            )

    @comms.Cog.listener()
    async def on_command_completion(self, ctx):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''UPDATE Commands SET completed=$2 WHERE jump=$1''',
                ctx.message.jump_url, datetime.now()
            )

    @comms.command()
    async def rank(self, ctx, user: discord.User = None):
        """Gets rank information about the user.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            user (discord.User): The user that will have their information retrieved (defaulted to None).

        """
        user = user if user is not None else ctx.author
        async with self.bot.pool.acquire() as conn:
            messages = await conn.fetch(
                '''SELECT jump FROM Messages WHERE id = $1''',
                user.id
            )
            commands = await conn.fetch(
                '''SELECT jump FROM Commands WHERE id = $1''',
                user.id
            )
        embed = discord.Embed(title=f'***Calculated rank for {user.name}:***')
        desc_lst = [
            f'Total commands executed: {len(commands)}',
            f'Total messages: {len(messages)}'
        ]
        embed.description = gen_block(desc_lst, lines=True)
        await ctx.send(embed=embed)

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
            tmp = str((datetime.min + v).time()).split(':')
            t[k] = ', '.join(f'{int(float(tmp[i]))} {timestamps[i]}' for i in range(
                len(timestamps)) if float(tmp[i]) != 0.0)

        # Inserting the login time for the bot.
        login = self.bot.startup_time.strftime('%A %I:%M:%S%p').lower().capitalize().replace(" ", " at ")

        t = {'login_time': login, **t}

        # Putting everything together for formatting.
        lst = [f'Login time', f'Average uptime', f'Longest uptime', f'Shortest uptime']
        lst = [f'{y[0]}: {y[1]}' for y in zip(lst, t.values())]
        lst = '\n'.join(str(y) for y in lst)

        embed = discord.Embed(title='*Bot uptime information:*', description=f'```py\n{lst}\n```')
        await ctx.send(embed=embed)

    @comms.command()
    async def since(self, ctx, *, name: str):
        async with self.bot.pool.acquire() as conn:
            d = await conn.fetch(
                '''SELECT t FROM Dates WHERE name = $1''', name
            )
            if len(d):
                delta = datetime.now() - d[0]['t']
                await ctx.send(f'{delta} since "{name}", {d}')
            else:
                await ctx.send(f'Could not find dated named "{name}"')

    @comms.command()
    @comms.is_owner()
    async def create_date(self, ctx, name, *, d: str = None):
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO Dates(t, id, name) VALUES ($1, $2, $3)''',
                datetime.now() if not d else datetime(*[int(x) for x in d.split()]),
                ctx.author.id, name
            )


def setup(bot):
    bot.add_cog(Records(bot))
