"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import iso8601
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from tabulate import tabulate

from modules import gen_block, http_get


class Covid19(comms.Cog):
    """Getting statistics of COVID-19 around the globe.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.cooldown(1, 10, BucketType.user)
    @comms.command(aliases=['corona'])
    async def COVID(self, ctx, *, option: str = None):
        """Getting information about either a country or the entire globe.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]covid US
            >>> [prefix]covid global
            >>> [prefix]covid United States of America

        """
        info = await http_get('https://api.covid19api.com/summary', session=self.bot.session)
        if option != 'global':
            found = False
            for i in info['Countries']:
                if option in i.values():
                    info, found = i, True
                    break
            if not found:
                return await ctx.send('`Could not find area.`')

            info = {k: v for i, (k, v) in enumerate(info.items()) if i > 2}
            tmp = iso8601.parse_date(info['Date'])
            info['Date'] = datetime.strftime(tmp, '%b %d %Y, %A %I:%M:%S%p').lower().capitalize()

        else:
            info = info['Global']

        lst = {}
        for k, v in info.items():
            # camelCase parser
            k = [f' {x}' if i > 0 and x.isupper() else x for i, x in enumerate(k)]
            lst[''.join(str(y) for y in k)] = v

        block = gen_block(tabulate(lst.items(), ['Title', 'Cases']).split('\n'))
        await ctx.send(block)


def setup(bot):
    bot.add_cog(Covid19(bot))
