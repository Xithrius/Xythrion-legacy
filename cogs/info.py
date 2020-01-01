"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


class Info_Director(comms.Cog):
    """Cog is meant to give information about owner and bot interactions."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot.

        Returns:
            The invite link so the bot can be invited to a server.

        """
        info = [
            'https://discordapp.com/oauth2/authorize?client_id=',
            self.bot.user.id,
            '&scope=bot&permissions=32885952'
        ]
        await ctx.send(''.join(str(y) for y in info))

    @comms.command()
    async def about(self, ctx):
        """Returns information about this bot's origin

        Returns:
            An embed object with links to creator's information.

        """
        info = {
            'Twitter': 'https://twitter.com/_Xithrius',
            'Github': 'https://github.com/Xithrius/Xythrion'
        }
        embed = discord.Embed(title='Project creation date: March 30, 2019',
                              description='\n'.join(
                                  f'[`{k}`]({v})' for k, v in info.items()))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info_Director(bot))
