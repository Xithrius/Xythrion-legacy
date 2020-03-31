"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType

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
        """Gets Warframe information.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            item (str): What service you would like to request from in the Warframe API.
            platform (str, optional): The platform that the user is on.

        Examples:
            >>> (ctx.prefix)warframe cetusCycle
            "cetusCycle" information:
            000 | id ~> cetusCycle1584763500000
            001 | expiry ~> 2020-03-21 04:05:00.000
            002 | activation ~> 2020-03-21 02:25:00.000
            003 | isDay ~> True
            004 | state ~> day
            005 | timeLeft ~> 23m 30s
            006 | isCetus ~> True
            007 | shortString ~> 23m to Night

            >>> (ctx.prefix)warframe earthCycle
            "earthCycle" information:
            000 | id ~> earthCycle1584763200000
            001 | expiry ~> 2020-03-21 04:00:00.140
            002 | activation ~> 2020-03-21 00:00:00.140
            003 | isDay ~> True
            004 | state ~> day
            005 | timeLeft ~> 18m 29s

        """
        if item not in self.options:
            embed = discord.Embed(title=f'"{item}" is not within option list.')
            embed.description = f'`Please pick from the following:`\n{gen_block(self.options, lines=True)}'
            return await ctx.send(embed=embed)

        url = f'https://api.warframestat.us/{platform}/{item}'
        info = await http_get(url, session=self.bot.session)

        for k, v in info.items():
            if k in ['expiry', 'activation']:
                x = [x if x in [':', '-', '.'] or x.isdigit() else ' ' for x in list(v)]
                info[k] = ''.join(str(y) for y in x)

        info = [f'{k} ~> {v}'.strip() for k, v in info.items()]

        embed = discord.Embed(title=f'"{item}" information:')
        embed.description = gen_block(info, lang='py', lines=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Warframe(bot))
