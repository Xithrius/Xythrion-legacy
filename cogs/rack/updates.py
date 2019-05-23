'''
>> Rehasher.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import platform

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.pathing import path
from rehasher.containers.QOL.shortened import now
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Update cog
# //////////////////////////////////////////////////////////////////////////// #
# Listens for updates to certien things
# //////////////////////////////////////////////////////////////////////////// #


class UpdatesCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Events

    """
    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Announces when the client joins a guild
        """
        printc(f'WARNING: CLIENT HAS JOINED GUILD {guild}')

    @comms.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Messages the owner when removed from a guild
        """
        try:
            await guild.owner.send(content=f'Goodbye, human', file=discord.File(path('rehasher', 'misc', 'images', 'removed.jpg')))
        except discord.errors.Forbidden:
            pass
        printc(f'WARNING: CLIENT HAS BEEN REMOVED FROM GUILD {guild}')

    @comms.Cog.listener()
    async def on_member_join(self, member):
        """
        Welcome the new member to the guild
        """
        embed = discord.Embed(name=f'Welcome to {member.guild}!', value=f'Owner: {member.guild.owner}', colour=0xc27c0e, timestamp=now())
        embed.add_field(name=f'Greetings, {member.name}!', value='Like, prepare to do things and stuff man', inline=False)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await member.send(embed=embed, file=discord.File(path('media', 'images', 'join.jpg')))
        role = discord.utils.get(member.guild.roles, name='Human')
        await member.add_roles(role)

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        """
        Laugh at the one who got banned
        """
        print(f'WARNING: {user.name} WAS BANNED FROM {guild.name}')
        try:
            await user.send(content=f'You have been banned from the server {guild.name}', file=discord.File(path('rehasher', 'misc', 'images', 'removed.jpg')))
        except discord.errors.Forbidden:
            pass

    @comms.Cog.listener()
    async def on_member_unban(self, guild, user):
        """
        Welcomes back a user
        """
        pass

    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Sends warning when there's an update in the status of a member
        """
        pass

    @comms.Cog.listener()
    async def on_message(self, message):
        """
        Blocking and logging whatever happens on servers that client is present on
        """
        try:
            if message.attachments[0].filename in ['.jpg', '.png', '.jpeg', '.gif'] and message.channel.topic == 'No pictures':
                await message.delete()
                await message.author.send(f'No pictures in channel {message.channel} of the server {message.guild}!')
        except (IndexError, AttributeError):
            pass
        except discord.errors.Forbidden:
            await message.guild.owner.send(f'I should be able to remove pictures from a channel that does not want any. Please give me the permissions to do so.')
        if message.author.id != self.bot.user.id:
            if len(message.embeds) >= 1 and message.channel.topic == 'No embeds':
                await message.delete()


def setup(bot):
    bot.add_cog(UpdatesCog(bot))
