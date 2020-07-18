"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import typing as t
from datetime import datetime
from pathlib import Path

import discord
from humanize import naturaldelta, intcomma, naturaldate
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from xythrion.utils import fancy_embed, markdown_link, parallel_executor, asteriks as ast


class Links(comms.Cog):
    """Links to many different things around the internet, including bot statistics.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific functions """

    @parallel_executor
    def calculate_lines(self) -> int:
        """Gets the sum of lines from all the python files in this directory

        Returns:
            int: The sum of the amount of lines within each .py file.

        """
        lst = []
        amount = 0

        for root, _, files in os.walk(Path.cwd() / self.bot.n):
            for file in files:
                if file.endswith('.py'):
                    lst.append(os.path.join(root, file))

        for file in lst:
            with open(file) as f:
                amount += sum(1 for _ in f)

        return intcomma(amount)

    async def calculate_uptime(self) -> dict:
        """Gets the uptime based off of information from the database.

        Returns:
            dict: Containing average, maximum, and minimum uptimes.

        """
        async with self.bot.pool.acquire() as conn:
            t = await conn.fetch(
                '''SELECT avg(t_logout - t_login) avg_uptime,
                          max(t_logout - t_login) max_uptime,
                          min(t_logout - t_login) min_uptime FROM Runtime''')

        t = {**{'t_uptime': datetime.now() - self.bot.startup_time}, **dict(t[0])}
        new_keys = ['Current uptime', 'Average', 'Maximum', 'Minimum']

        t = {k: naturaldelta(v) for k, v in zip(new_keys, t.values())}

        return [f'{ast(k)}: {v}' for k, v in t.items()]

    async def get_links(self) -> t.List[str]:
        """Provides links about the creator and bot.

        Returns:
            :obj:`t.List[str]`: A list containing Discord markdown hyperlinks.

        """
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        return [markdown_link(k, v) for k, v in info.items()]

    async def get_date_of_creation(self) -> t.List[str]:
        d = datetime(2019, 3, 13, 17, 16)

        t = {
            'Started:': f"{naturaldate(d)}. {naturaldelta(datetime.now() - d, months=False)} ago."
        }

        return [f'{ast(k)}: {v}' for k, v in t.items()]

    """ Commands """

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command(aliases=['uptime', 'runtime', 'desc', 'description'])
    async def info(self, ctx: comms.Context) -> None:
        """Information about bot origin along with usage statistics.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: None

        Command examples:
            >>> [prefix]info

        """
        _links = await self.get_links()
        _line_amount = await self.calculate_lines()
        _uptime = await self.calculate_uptime()
        _dates = await self.get_date_of_creation()

        d = {
            'Links:': _links,
            'Lines of Python code:': [_line_amount],
            'Uptime information:': _uptime,
            'Project length:': _dates
        }

        await ctx.send(embed=fancy_embed(d))

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            :obj:`type(None)`: None

        Command examples:
            >>> [prefix]invite

        """
        _id = self.bot.user.id
        permissions = {'Sending and reacting': 19520,
                       'Previous + removing messages': 27712,
                       'Administrator (not needed)': 8}
        url = f'https://discordapp.com/oauth2/authorize?client_id={_id}&scope=bot&permissions='
        invite_urls = {k: f'{url}{v}' for k, v in permissions.items()}
        invite_urls = '\n'.join(markdown_link(k, v) for k, v in invite_urls.items())

        embed = discord.Embed(description='`Invite urls:`\n' + invite_urls)

        await ctx.send(embed=embed)


def setup(bot: comms.Bot) -> None:
    """The necessary function for loading in cogs within this file.

    Args:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    Returns:
        type(None): Always None.

    """
    bot.add_cog(Links(bot))
