"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import time
from datetime import datetime

import discord
import psutil
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from psutil._common import bytes2human as b2h

from modules import (
    ast, describe_date, gen_block, join_mapped, markdown_link, path,
    parallel_executor
)


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

    """ Cog-specific functions """

    def calculate_lines(self) -> int:
        """Gets the sum of lines from all the python files in this directory

        Returns:
            An integer with the sum of the amount of lines within each .py file.

        """
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

    async def calculate_uptime(self) -> str:
        """Gets the uptime based off of information from the database.

        Returns:
            A list containing all uptime information.

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
        lst = ['UPTIME:'] + [f'{" " * 5}{y[0]}: {y[1]}' for y in zip(lst, t.values())]

        return join_mapped(lst) + '\n'

    @parallel_executor
    def calculate_usage(self) -> str:
        """Gets the usage of the CPU and ram.

        Returns:
            A formatted string for the code block.

        """
        d = describe_date(datetime.now() - datetime(year=2019, month=3, day=13, hour=17, minute=16))

        mem = psutil.virtual_memory()
        # cpu = {
        #     'Usage': f'{psutil.cpu_percent(interval=100)}%',
        #     'Cores': psutil.cpu_count()
        # }
        cpu = [
            f'Usage: {psutil.cpu_percent(interval=1)}%',
            f'Cores: {psutil.cpu_count()}'
        ]
        tags = ['percent', 'total', 'available', 'used']

        ram = [
            b2h(mem.__getattribute__(m)) if m != 'percent' else f'{mem.__getattribute__(m)}%' for m in tags
        ]
        ram = [f'{t.capitalize()}: {r}' for t, r in zip(tags, ram)]

        lines = self.calculate_lines()
        users = sum([len(guild.members) for guild in self.bot.guilds])
        info = [
            f'Project created {d} ago, on March 13, 2019, 5:19pm PDT.',
            f'Bot currently contains {lines} lines of Python code.',
            f'Running on {len(self.bot.guilds)} servers ({users} users).'
        ]

        titles = ['INFORMATION:', 'CPU:', 'RAM']
        lst = [info, cpu, ram]
        lst = [f'{t}\n{join_mapped(" " * 5 + y for y in l)}\n' for t, l in zip(titles, lst)]

        return join_mapped(lst)

    async def calculate_latency(self) -> str:
        """Calculates and recieves different amounts of latency.

        Returns:
            A string with 3 different types of latency.

        """
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

        return f'LATENCY:\n{join_mapped(" " * 5 + y for y in lst)}\n'

    async def get_links(self) -> discord.Embed:
        """Creates an embed full of links about the bot.

        Returns:
            A embed object containing description links.

        """
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            f'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }
        info = '\n'.join(markdown_link(k, v) for k, v in info.items())

        return discord.Embed(
            title=ast('Links:'),
            description=info
        )

    """ Commands """

    @comms.cooldown(1, 1, BucketType.user)
    @comms.command()
    async def info(self, ctx):
        """Information about bot origin along with usage statistics.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            option (str, optional): Whatever information about the bot the user could want.

        Command examples:
            >>> [prefix]info
            >>> [prefix]info ping

        """

        lst = [
            await self.calculate_latency(),
            await self.calculate_usage(),
            await self.calculate_uptime()
        ]

        await ctx.send(content=gen_block(lst), embed=await self.get_links())

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]invite

        """
        _id = self.bot.user.id
        url = f'https://discordapp.com/oauth2/authorize?client_id={_id}&scope=bot&permissions=37604544'
        embed = discord.Embed(description=markdown_link('Xythrion invite url', url))
        await ctx.send(embed=embed)

    @comms.command()
    async def links(self, ctx):
        """Lists out all the available links in the database.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]links

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT name FROM Links''',
            )
            info = [i['name'] for i in info]

            embed = discord.Embed(
                title='**All link names:**',
                description=gen_block(info, lines=True)
            )
            await ctx.send(embed=embed)

    @comms.cooldown(1, 1, BucketType.user)
    @comms.command()
    async def link(self, ctx, name: str, content: str = None):
        """Gets the content of a link, and if you are the owner of the bot, add links.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            name (str): The name of the link to find within the database, or make a new link for.
            content (str, optional): The content that the link will be named under.

        Command examples:
            >>> [prefix]link "odd future"
            >>> [prefix]link "forbidden" https://http.cat/403.jpg

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT link, t, id FROM Links WHERE name = $1''',
                name
            )
            if len(info):
                if content:
                    await ctx.send('`That name already exists within the database.`')

                else:
                    _link = info[0]['link']
                    if _link[-4:] in ('.jpg', 'jpeg', '.png'):
                        embed = discord.Embed(
                            description=markdown_link(name, _link)
                        )
                        embed.set_image(url=_link)
                        return await ctx.send(embed=embed)
                    await ctx.send(_link)

            else:
                if content:
                    # Only the owner of the bot can create new links.
                    if await self.bot.is_owner(ctx.author):
                        await conn.execute(
                            '''INSERT INTO Links(t, id, name, link) VALUES ($1, $2, $3, $4)''',
                            datetime.now(), ctx.author.id, name, content
                        )
                    else:
                        raise comms.NotOwner

                else:
                    await ctx.send('`Sorry, but a link with that name could not be found.`')

    @comms.command(hidden=True)
    @comms.is_owner()
    async def remove_link(self, ctx, name: str):
        """Removes a link from the database.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            name (str): The name of the link to find within the database.

        Command examples:
            >>> [prefix]remove_link "odd future"

        """
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                '''DELETE FROM links WHERE name = $1''',
                name
            )


def setup(bot):
    bot.add_cog(Links(bot))
