"""
>> LogistiX
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


class Identity_Cog(comms.Cog):
    """ Commands with a small amount of personality """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Commands """

    @comms.command()
    async def creator(self, ctx):
        """ Shows the person who created the bot """
        embed = discord.Embed(colour=0xc27c0e)
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Private Github:', value='[Right here](https://github.com/Xithrius/Relay.py)')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='icon')
    async def get_own_avatar(self, ctx):
        """ The avatar of the bot """
        await ctx.send(self.bot.user.avatar_url)


def setup(bot):
    bot.add_cog(Identity_Cog(bot))
