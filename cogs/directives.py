'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries
# /////////////////////////////////////////////////////////
# Built-in modules, third-party modules, custom modules
# //////////////////////////////////////////////////////////////////////////// #


import time

import discord
from discord.ext import commands as comms


# //////////////////////////////////////////////////////////////////////////// #
#
# /////////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////////////////////////// #


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# //////////////////////// # Commands
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

# //////////////////////// # Events
    @comms.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(name=f'Welcome to {member.guild}!', value=f'Owner: {member.guild.owner}')
        member.send(embed=embed)

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} was banned from {guild.name}')
        await user.channel.send(f'{user.name} was banned from {guild.name}')


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
