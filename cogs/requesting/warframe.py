"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import discord
import iso8601
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from tabulate import tabulate

from modules import gen_block, http_get


class Warframe(comms.Cog):
    """Getting information from the Warframe service

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.
        options (list): A list of titles of information to be requested from warframe.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot
        self.options = [
            'cetusCycle',
            'earthCycle',
            'vallisCycle'
        ]

    """ Commands """

    @comms.cooldown(1, 3, BucketType.user)
    @comms.command()
    async def warframe(self, ctx, item: str, platform: str = 'pc'):
        """Gets information about Warframe items and cycles.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            item (str): What service you would like to request from in the Warframe API.
            platform (str, optional): The platform that the user is on.

        Command examples:
            >>> [prefix]warframe cetusCycle
            >>> [prefix]warframe earthCycle

        """
        if item not in self.options:
            embed = discord.Embed(title=f'"{item}" is not within option list.')
            embed.description = f'`Please pick from the following:`\n{gen_block(self.options, lines=True)}'
            return await ctx.send(embed=embed)

        url = f'https://api.warframestat.us/{platform}/{item}'
        info = await http_get(url, session=self.bot.session)

        for k, v in info.items():
            if k in ['expiry', 'activation']:
                v = iso8601.parse_date(v)
                info[k] = datetime.strftime(v, '%b %d %Y, %A %I:%M:%S%p').lower().capitalize()

        block = gen_block(tabulate(info.items()).split('\n'))
        await ctx.send(block)


def setup(bot):
    bot.add_cog(Warframe(bot))
