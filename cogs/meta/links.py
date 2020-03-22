"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Links(comms.Cog):
    """Links that I think are important.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

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
    async def info(self, ctx):
        """Returns information about this bot's origin

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        """
        d = abs(datetime.datetime(year=2019, month=3, day=13) - datetime.datetime.now()).days
        branch_link = 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e'
        info = {
            f'Project created {d} days ago, on March 13, 2019': branch_link,
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius'
        }
        embed = discord.Embed(description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()))
        await ctx.send(embed=embed)

    @comms.command()
    async def link(self, ctx, name: str, *, content: str = None):
        pass


def setup(bot):
    bot.add_cog(Links(bot))
