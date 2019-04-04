'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import datetime
import time
import sys

import discord
from discord.ext import commands as comms

# from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
# Directives cog
# ////////////////////////
# General commands, that is all
# ///////////////////////////////////////////////////////// #


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
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
        try:
            if 'log' == sys.argv[1]:
                print(f"guild: '{message.guild}', channel: '{message.channel}', user: '{message.author}' sends:\n\t[{now}]  '{message.content}'")
        except IndexError:
            pass
        pic_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        for extension in pic_extensions:
            try:
                if message.attachments[0].filename.endswith(extension) and message.channel.topic == 'No pictures':
                    await message.delete()
                    await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
            except IndexError:
                pass
            except discord.errors.Forbidden:
                await message.guild.owner.send(f'I should be able to remove pictures from a channel that does not want any. Please give me the permissions to do so.')

    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        now = datetime.datetime.now() + datetime.timedelta(hours=8)
        try:
            if 'log' == sys.argv[1]:
                print()
        except IndexError:
            pass


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
