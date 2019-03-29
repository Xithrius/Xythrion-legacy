# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Uses the virtual environment
# The package 'essentials' is customly-made
# ///////////////////////////////////////////////////////// #


from discord.ext import commands as comms
import discord
import datetime
import time

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt

# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


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

    @comms.command(name='users')
    @comms.guild_only()
    async def get_members(self, ctx):
        await ctx.send(f"Members on this server: {', '.join(str(x) for x in ctx.message.guild.members)}")

# Events
    @comms.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(name=f'Welcome to {member.guild}!', value=f'Owner: {member.guild.owner}')
        member.send(embed=embed)

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} was banned from {guild.name}')
        await user.channel.send(f'{user.name} was banned from {guild.name}')

    @comms.Cog.listener()
    async def on_message(self, message):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        print(f"guild: '{message.guild}', channel: '{message.channel}', user: '{message.author}' sends:\n\t[{now}]  '{message.content}'")
        pic_extensions = ['.jpg', '.png', '.jpeg']
        for extension in pic_extensions:
            try:
                if message.attachments[0].filename.endswith(extension) and message.channel.topic == 'No pictures':
                    await message.delete()
                    await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
            except IndexError:
                pass
            except discord.errors.Forbidden:
                await message.guild.owner.send(f'I should be able to remove pictures from a channel that does not want any. Please give me the permissions to do so.')


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
