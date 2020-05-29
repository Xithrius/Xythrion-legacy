"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import typing as t

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

from utils import path, markdown_link, parallel_executor


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

    @parallel_executor
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
        return t

    async def get_links(self) -> t.List[str]:
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            f'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        return [markdown_link(k, v) for k, v in info.items()]

    """ Commands """

    @comms.cooldown(1, 1, BucketType.user)
    @comms.command(aliases=['uptime', 'desc', 'description'])
    async def info(self, ctx):
        """Information about bot origin along with usage statistics.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            option (str, optional): Whatever information about the bot the user could want.

        Command examples:
            >>> [prefix]info
            >>> [prefix]info ping

        """
        _amount = await self.calculate_lines()
        _links = await self.get_links()
        # NOTE: Parse times sometime.
        _uptime = await self.calculate_uptime()

        # await ctx.send(embed=embed)

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


def setup(bot):
    bot.add_cog(Links(bot))
