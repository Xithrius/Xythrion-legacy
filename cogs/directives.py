from discord.ext import commands as comms
import discord
import datetime
import time


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='owner')
    async def show_creator(self, ctx):
        embed = discord.Embed(colour=0xc27c0e)
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Private Github:', value='[Right here](https://github.com/Xithrius/Demonically)')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='ping')
    async def get_latency(self, ctx):
        timeStart = time.time()
        await ctx.trigger_typing()
        timeEnd = time.time()
        timeTaken = timeEnd - timeStart
        await ctx.send(f'Took {timeTaken} seconds to complete')


# Events
    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        """ """
        print(f'{user.name} was banned from {guild.name}')
        await user.channel.send(f'{user.name} was banned from {guild.name}')

    @comms.Cog.listener()
    async def on_message(self, message):
        """ """
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        print(f'[{now}]  {message.author}: {message.content}')


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
