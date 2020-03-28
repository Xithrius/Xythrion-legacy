"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import os
import time
import typing as t
from datetime import datetime

import discord
import psutil
from discord.ext import commands as comms
from psutil._common import bytes2human as b2h

from modules import describe_date, gen_block, lock_executor, path


class Links(comms.Cog):
    """Links to many different things around the internet, including bot statistics.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    def calculate_lines(self):
        """ """
        lst = []
        amount = 0
        for root, dirs, files in os.walk(path()):
            for file in files:
                if file.endswith('.py'):
                    lst.append(os.path.join(root, file))

        for file in lst:
            with open(file) as f:
                amount += sum(1 for _ in f)

        return amount

    async def calculate_uptime(self):
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
        lst = ['UPTIME:'] + [f'{" " * 5}{y[0]}: {y[1]}' for y in zip(lst, t.values())]

        return lst

    async def get_usage(self):
        d = describe_date(datetime.now() - datetime(year=2019, month=3, day=13, hour=17, minute=16))

        mem = psutil.virtual_memory()
        cpu = {
            'Usage': f'{psutil.cpu_percent(interval=None)}%',
            'Cores': psutil.cpu_count()
        }
        cpu = [
            f'Usage: {psutil.cpu_percent(interval=None)}%',
            f'Cores: {psutil.cpu_count()}'
        ]
        tags = ['percent', 'total', 'available', 'used']

        ram = [
            b2h(mem.__getattribute__(m)) if m != 'percent' else f'{mem.__getattribute__(m)}%' for m in tags
        ]
        ram = [f'{t.capitalize()}: {r}' for t, r in zip(tags, ram)]

        lines = await lock_executor(self.calculate_lines)
        users = sum([len(guild.members) for guild in self.bot.guilds])
        info = [
            f'Project created {d} ago, on March 13, 2019, 5:19pm PDT.',
            f'Bot currently contains {lines} lines of Python code.',
            f'Running on {len(self.bot.guilds)} servers ({users} users).'
        ]

        info = '\n'.join(' ' * 5 + y for y in info)
        cpu = '\n'.join(' ' * 5 + y for y in cpu)
        ram = '\n'.join(' ' * 5 + y for y in ram)

        lst = [
            f'INFORMATION:\n{info}\n',
            f'CPU:\n{cpu}\n',
            f'RAM:\n{ram}'
        ]

        return lst

    async def calculate_latency(self):
        start = time.perf_counter()
        end = time.perf_counter()
        calculated_ping = (end - start) * 1000

        timeStart = time.time()
        timeEnd = time.time()
        timeTaken = timeEnd - timeStart

        lst = [
            f'Response time: {timeTaken}ms',
            f'Calculated ping: {calculated_ping}',
            f'Discord WebSocket protocol latency: {self.bot.latency}'
        ]

        lst = '\n'.join(' ' * 5 + y for y in lst)
        lst = [f'LATENCY:\n{lst}']

        return lst

    async def get_links(self):
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            f'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }
        info = '\n'.join(f'[`{k}`]({v})' for k, v in info.items())

        embed = discord.Embed(
            title='**Links:**',
            description=info
        )

        return embed

    @comms.command(aliases=['about', 'links', 'usage', 'ping', 'latency', 'information'])
    async def info(self, ctx):
        """Returns information about this bot's origin along with usage statistics.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        tmp = [await self.get_usage(), await self.calculate_uptime(), await self.calculate_latency()]
        lst = []
        for i in tmp:
            lst.extend(i + [''])

        embed = await self.get_links()

        await ctx.send(content=gen_block(lst).strip(), embed=embed)

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        _id = self.bot.user.id
        url = f'https://discordapp.com/oauth2/authorize?client_id={_id}&scope=bot&permissions=37604544'
        embed = discord.Embed(description=f'[`Xythrion invite url`]({url})')
        await ctx.send(embed=embed)

    @comms.command()
    async def link(self, ctx, name: str, *, content: t.Optional[str] = None):
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT link, t, id FROM Links WHERE name = $1''',
                name
            )
            if len(info):
                if content:
                    return await ctx.send('`Sorry, that link already exists.`')
                else:
                    # All users can access links, but none can create except the owner of the bot.
                    info = info[0]
                    embed = discord.Embed(
                        description=f'[`{name}`]({info["link"]})'
                    )
                    if info['link'][-4:] in ('.jpg', 'jpeg', '.png'):
                        embed.set_image(url=info['link'])

                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction('\U00002754')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) == '\U00002754'

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        pass
                    else:
                        embed.set_footer(text=f'Full link: {info["link"]}')
                        await msg.edit(embed=embed)

            else:
                # Only the owner of the bot can create new links.
                if content and await self.bot.is_owner(ctx.author):
                    await conn.execute(
                        '''INSERT INTO Links(t, id, name, link) VALUES ($1, $2, $3, $4)''',
                        datetime.now(), ctx.author.id, name, content
                    )
                    await ctx.send(f'`Link with name "{name}" successfully inserted into the database.`')

                else:
                    await ctx.send('`Sorry, could not find any link with that name.`')


def setup(bot):
    bot.add_cog(Links(bot))
