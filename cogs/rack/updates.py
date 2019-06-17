'''
>> SoftBot
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

from SoftBot.containers.QOL.pathing import path
from SoftBot.containers.QOL.shortened import now
from SoftBot.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Update cog
# //////////////////////////////////////////////////////////////////////////// #
# Listens for updates to certien things
# //////////////////////////////////////////////////////////////////////////// #


class Updates_Cog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        Misc setup background task
        """
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.misc_setup())
        self.presence = 'with info'

    """

    Background tasks

    """
    async def misc_setup(self):
        await self.bot.change_presence(activity=discord.Game(name=self.presence))

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
            await guild.owner.send(content=f'Goodbye, human', file=discord.File(path('SoftBot', 'misc', 'images', 'removed.jpg')))
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
            await user.send(content=f'You have been banned from the server {guild.name}', file=discord.File(path('SoftBot', 'misc', 'images', 'removed.jpg')))
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

        # Logging messages for charts and the COH leveling system
        if str(message.author) != str(self.bot.user):
            try:
                with open(path('repository', 'logs', f'{message.author}.txt'), 'a') as f:
                    f.write(f'{message.created_at}~~~{message.guild}\n')
                with open(path('repository', 'logs', f'{message.author}.txt'), 'r') as f:
                    length = len(f.readlines())
                    if length == 1:
                        embed = discord.Embed(title=f'`Leveling system activated for user {message.author}!`', colour=0xc27c0e, timestamp=now())
                        info = '''
                        `You have been initiated to ascend into the next circles of hell!`
                        `You're currently starting at level 1, the first circle of hell.`
                        `Good luck on ascending to the next levels~`
                        '''
                        embed.add_field(name='`Circles of hell`:', value=info)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await message.channel.send(embed=embed)
                    elif length % 75 == 0:
                        embed = discord.Embed(title=f'`User {message.author} has ascended!`', colour=0xc27c0e, timestamp=now())
                        info = f'''
                        {message.author.mention} `stats`:
                        `Circle of hell reached`: `Level {int(length / 75)}`
                        `Total messages sent:` `{length}`
                        '''
                        embed.add_field(name='`Circles of hell`:', value=info)
                        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
                        await message.channel.send(embed=embed)
            except FileNotFoundError:
                with open(path('repository', 'logs', f'{message.author}.txt'), 'w') as f:
                    f.write(f'{message.created_at}~~~{message.guild}\n')

    """

    Commands

    """
    @comms.command(name='rank')
    async def check_COH_rank(self, ctx):
        levels = len((open(path('repository', 'logs', f'{ctx.message.author}.txt'), 'r')).readlines())
        embed = discord.Embed(title=f'`Current circle of hell for user {ctx.message.author}`', colour=0xc27c0e, timestamp=now())
        info = f'''
        {ctx.message.author.mention} `stats`:
        `Current circle of hell`: `Level {round((levels / 75), 4)}`
        `Total messages sent:` `{levels}`
        '''
        embed.add_field(name='`Info`:', value=info)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Updates_Cog(bot))
