'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import time
import platform
import datetime

from discord.ext import commands as comms
import discord

from containers.essentials.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Directives cog
# //////////////////////////////////////////////////////////////////////////// #
# A place for all general but simple commands to go
# //////////////////////////////////////////////////////////////////////////// #


class DirectivesCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s): bot """
        self.bot = bot

# //////////////////////////////////////////////// # Commands

    @comms.command(name='ping')
    async def get_latency(self, ctx):
        """ Get ping for the bot to the nearest discord server """
        timeStart = time.time()
        await ctx.trigger_typing()
        timeEnd = time.time()
        timeTaken = timeEnd - timeStart
        await ctx.send(f'Took {timeTaken} seconds to complete')

    @comms.command(name='members')
    @comms.guild_only()
    async def get_members(self, ctx):
        """ Get all users that exist within the guild """
        await ctx.send(f"Members on this server: {', '.join(str(x) for x in ctx.message.guild.members)}")

# //////////////////////////////////////////////// # Events

    @comms.Cog.listener()
    async def on_member_join(self, member):
        """ Welcome the new member to the guild """
        embed = discord.Embed(name=f'Welcome to {member.guild}!', value=f'Owner: {member.guild.owner}', colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=8))
        embed.add_field(name=f'Greetings, {member.name}!', value='Like, prepare to do things and stuff man', inline=False)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await member.send(embed=embed, file=discord.File(path('relay', 'misc', 'images', 'join.jpg')))

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        """ Laugh at the one who got banned """
        print(f'WARNING: {user.name} WAS BANNED FROM {guild.name}')
        try:
            await user.send(content=f'You have been banned from the server {guild.name}', file=discord.File(path('relay', 'misc', 'images', 'removed.jpg')))
        except discord.errors.Forbidden:
            pass

    @comms.Cog.listener()
    async def on_member_unban(guild, user):
        """ Welcomes back a user """
        pass

    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        """ Announces when the client joins a guild """
        pass

    @comms.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Messages the owner when removed from a guild """
        try:
            await guild.owner.send(content=f'Goodbye, human', file=discord.File(path('relay', 'misc', 'images', 'removed.jpg')))
        except discord.errors.Forbidden:
            pass

    @comms.Cog.listener()
    async def on_message(self, message):
        """ Blocking and logging whatever happens on servers that client is present on """
        # Blocking pictures if the description doesn't want them
        pic_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        for extension in pic_extensions:
            try:
                if message.attachments[0].filename.endswith(extension) and message.channel.topic == 'No pictures':
                    await message.delete()
                    await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
            except IndexError or AttributeError:
                pass
            except discord.errors.Forbidden:
                await message.guild.owner.send(f'I should be able to remove pictures from a channel that does not want any. Please give me the permissions to do so.')


def setup(bot):
    bot.add_cog(DirectivesCog(bot))
