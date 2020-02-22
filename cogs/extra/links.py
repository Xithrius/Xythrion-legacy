"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Links(comms.Cog):
    """Many useful links are given by this cog."""

    def __init__(self, bot):
        self.bot = bot

    @comms.command(aliases=['google'])
    async def lmgtfy(self, ctx, *, search_term: str):
        """Gives a link of the 'let me google that for you' website.

        Args:
            search_term (str): A string of whatever the user wants the link to contain.

        Returns:
            A link of https://lmgtfy.com with custom arguments (internet explainer always included) 

        """
        search = search_term.replace(' ', '+')
        url = f'https://lmgtfy.com/?q={search}&iie=1'
        embed = discord.Embed(description=f'[`{search_term}`]({url})')
        await ctx.send(embed=embed)

    @comms.command()
    async def eternal(self, ctx):
        """Gives release information for Doom Eternal.

        Returns:
            An embed with the date of release and how many days until.

        """
        d = abs(datetime.datetime(year=2020, month=3, day=20) - datetime.datetime.now()).days
        embed = discord.Embed(description=f'Raze hell in `{d}` days.')
        embed.set_thumbnail(url='https://i.imgur.com/Y57XrCu.png')
        embed.set_footer(text=f'(Doom eternal is released in {d} days from now.)')
        await ctx.send(embed=embed)

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Returns:
            The invite link so the bot can be invited to a server.

        """
        url = f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=37604544'
        embed = discord.Embed(description=f'[`Xythrion invite url`]({url})')
        await ctx.send(embed=embed)

    @comms.command()
    async def info(self, ctx):
        """Returns information about this bot's origin

        Returns:
            An embed object with links to creator's information.

        """
        d = abs(datetime.datetime(year=2019, month=3, day=13) - datetime.datetime.now()).days
        info = {
            f'Project created {d} days ago, on March 13, 2019': 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e',
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius'
        }
        embed = discord.Embed(description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Links(bot))
