from discord.ext import commands as comms
import discord
import datetime
import time


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command()
    async def poke(self, ctx, member: discord.User = None):
        if member is None:
            await ctx.author.send('Hi')
        else:
            possibleMembers = []
            _members = ctx.message.guild.members
            for i in range(len(_members)):
                if _members[i].startswith(member):
                    possibleMembers.append(_members[i])
            await ctx.send(ctx.message.discord.User)
            if len(possibleMembers) > 1:
                await ctx.send(f"Searched member {member} has multiple possibilities: {', '.join(str(x) for x in possibleMembers)}")
            if len(possibleMembers) == 1:
                member = discord.User(possibleMembers)
                await ctx.member.send("Testing stuff")

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
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} was banned from {guild.name}')
        await user.channel.send(f'{user.name} was banned from {guild.name}')

    @comms.Cog.listener()
    async def on_message(self, message):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        print(list(message.content))
        print(f'[{now}]  {message.author}: {message.content}')
        pic_extensions = ['.jpg', '.png', '.jpeg']
        for extension in pic_extensions:
            try:
                if message.attachments[0].filename.endswith(extension) and message.channel.topic == 'No pictures':
                    await message.delete()
                    await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
            except IndexError:
                pass


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
