"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime

import discord
from discord.ext import commands as comms


class Links(comms.Cog):
    """Cog is meant to give information about owner and bot interactions."""

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    async def doom(self, ctx):
        """Gives the best song for doom, at the perfect time
        
        Returns:
            An embed with a youtube link containing the best drop in the best game.

        """
        url = 'https://youtu.be/LGNc5azoizI?t=353'
        embed = discord.Embed(description=f'[`Raze hell`]({url})')
        await ctx.send(embed=embed)

    @comms.command()
    async def eternal(self, ctx):
        """Gives release information for Doom Eternal.

        Returns:
            An embed with the date of release and how many days until.

        """
        d = abs(datetime.datetime(year=2020, month=3, day=20) - datetime.datetime.now()).days
        embed = discord.Embed(title='Raze Hell.', description=f'`{d}` days remaining until release on March 20, 2020')
        embed.set_thumbnail(url='https://i.imgur.com/Y57XrCu.png')
        await ctx.send(embed=embed)

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Returns:
            The invite link so the bot can be invited to a server.

        """
        url = f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=969920'
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
            f'Project created `{d}` days ago, on `March 13, 2019`': 'https://github.com/Xithrius/Xythrion/tree/55fe604d293e42240905e706421241279caf029e',
            'Xythrion Github repository': 'https://github.com/Xithrius/Xythrion',
            "Xithrius' Twitter": 'https://twitter.com/_Xithrius',
            "Xithrius' Github": 'https://github.com/Xithrius'
        }
        embed = discord.Embed(description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Links(bot))