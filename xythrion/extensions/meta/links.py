"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
from typing import List
from datetime import datetime
from pathlib import Path

import discord
from humanize import naturaldelta, intcomma, naturaldate
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Cog, Context

from xythrion.utils import fancy_embed, markdown_link, parallel_executor
from xythrion.bot import Xythrion


class Links(Cog):
    """Links to many different things around the internet, including bot statistics."""

    def __init__(self, bot: Xythrion):
        self.bot = bot

    @parallel_executor
    def calculate_lines(self) -> int:
        """Gets the sum of lines from all the python files a directory."""
        lst = []
        amount = 0

        for root, _, files in os.walk(Path.cwd() / self.bot.n):
            for file in files:
                if file.endswith('.py'):
                    lst.append(os.path.join(root, file))

        for file in lst:
            with open(file) as f:
                amount += sum(1 for _ in f)

        return [intcomma(amount)]

    async def get_links(self) -> List[str]:
        """Provides links about the creator and bot."""
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            'First commit to the repository': branch_link,
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius',
            "Xithrius' Twitch": 'https://twitch.tv/Xithrius'
        }

        return [markdown_link(k, v) for k, v in info.items()]

    async def get_date_of_creation(self) -> List[str]:
        d = datetime(2019, 3, 13, 17, 16)

        return [f'{naturaldate(d)}; {naturaldelta(datetime.now() - d, months=False)} ago.']

    @comms.cooldown(1, 5, BucketType.user)
    @comms.command(aliases=['uptime', 'runtime', 'desc', 'description'])
    async def info(self, ctx: Context) -> None:
        """Information about bot origin along with usage statistics."""
        media_links = await self.get_links()
        amount_of_lines = await self.calculate_lines()
        project_length = await self.get_date_of_creation()

        d = {
            'Links:': media_links,
            'Lines of Python code:': amount_of_lines,
            'Current uptime:': [naturaldelta(datetime.now() - self.bot.startup_time)],
            'Project length:': project_length
        }

        await ctx.send(embed=fancy_embed(d))

    @comms.command()
    async def invite(self, ctx: Context) -> None:
        """Gives the invite link of this bot."""
        _id = self.bot.user.id
        permissions = {'Sending and reacting': 19520,
                       'Previous + removing messages': 27712,
                       'Administrator (not needed)': 8}
        url = f'https://discordapp.com/oauth2/authorize?client_id={_id}&scope=bot&permissions='
        invite_urls = {k: f'{url}{v}' for k, v in permissions.items()}
        invite_urls = '\n'.join(markdown_link(k, v) for k, v in invite_urls.items())

        embed = discord.Embed(description='`Invite urls:`\n' + invite_urls)

        await ctx.send(embed=embed)
