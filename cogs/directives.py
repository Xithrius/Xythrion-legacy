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
import platform
import datetime

from discord.ext import commands as comms
import discord

from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Directives cog
# ///////////////////////////////////////////////////////// #
# General commands for the general public
# //////////////////////////////////////////////////////////////////////////// #


class DirectivesCog(comms.Cog):

    # //////////////////////// # Object(s): bot
    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Get ping for the bot to the nearest discord server
    @comms.command(name='ping')
    async def get_latency(self, ctx):
        timeStart = time.time()
        await ctx.trigger_typing()
        timeEnd = time.time()
        timeTaken = timeEnd - timeStart
        await ctx.send(f'Took {timeTaken} seconds to complete')

    # //////////////////////// # Get all users that exist within the guild
    @comms.command(name='members')
    @comms.guild_only()
    async def get_members(self, ctx):
        await ctx.send(f"Members on this server: {', '.join(str(x) for x in ctx.message.guild.members)}")

# //////////////////////////////////////////////// # Events
    # //////////////////////// # Welcome the new member to the guild
    @comms.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(name=f'Welcome to {member.guild}!', value=f'Owner: {member.guild.owner}', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=8))
        embed.add_field(name=f'Greetings, {member.name}!', value='', inline=False)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await member.send(file=discord.File(path('misc', 'images', 'join.jpg')))
        await member.send(embed=embed)

    # //////////////////////// # Laugh at the one who got banned
    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} was banned from {guild.name}')
        await user.channel.send(f'{user.name} was banned from {guild.name}')


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
