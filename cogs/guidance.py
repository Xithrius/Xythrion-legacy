from discord.ext import commands as comms
import discord


class HelpCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# General help command
    @comms.group()
    async def help(self, ctx):
        embed = discord.Embed(colour=0xc27c0e)
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

# Directives cog
    @help.command(name='owner')
    async def show_creator(self, ctx):
        pass

# Passwords cog
    @help.command()
    async def random_password(self, ctx):
        pass


def setup(bot):
    bot.add_cog(HelpCog(bot))
