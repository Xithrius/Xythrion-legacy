import discord
from discord.ext import commands as comms
import random
import string
import datetime


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command()
    async def random_password(self, ctx, length=10, personal='true'):
        """ Random password of default length 10. '$random_password <length>'"""
        if length > 0:
            password = ''.join(str(y) for y in [random.choice(string.ascii_letters + string.digits) for i in range(length)])
            embed = discord.Embed(title="[ Random Password Generator ]", timestamp=datetime.datetime.now() + datetime.timedelta(hours=8), colour=0xc27c0e)
            embed.add_field(name=f"Password of length {length}:", value=password, inline=False)
            if personal == "true":
                await ctx.author.send(embed=embed, delete_after=30)
            else:
                await ctx.send(embed=embed, delete_after=180)
        else:
            if personal == "true":
                await ctx.author.send(f"{length} is an invalid parameter.")
            else:
                await ctx.send(f"{length} is an invalid parameter")

    @comms.command(name='creator')
    async def show_creator(self, ctx):
        embed = discord.Embed(colour=0xc27c0e)
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Private Github:', value='[Right here](https://github.com/Xithrius/Demonically)')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

# Events
    async def on_member_ban(self, guild, user):
        """ """
        print(f"{user.name}-{user.id} was banned from {guild.name}-{guild.id}")

    async def on_message(self, message):
        """ """
        print(message.content)


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
