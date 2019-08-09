"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import sqlite3
import json

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, printc


class Updates_Cog(comms.Cog):
    """ Waits for events to occur on servers  """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Misc setup background task
        """
        self.bot = bot
        self.db_path = path('repository', 'data', 'user_info.db')

    """ Database checking """

    def create_db(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE Users (id INTEGER UNIQUE, name TEXT NOT NULL, points INTEGER)''')
        self.conn.commit()
        self.conn.close()

    """ Events """

    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        """ Creating the leveling system for users when joining a guild, and also greeting them """
        printc(f'[WARNING]: CLIENT HAS JOINED GUILD {guild}')
        if not os.path.isfile(self.db_path):
            self.create_db()
        printc('[...]: SCANNING ALL USERS IN GUILD...')
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        members_added = 0
        for member in guild.members:
            try:
                c.execute('''INSERT INTO Users VALUES (?, ?, ?)''',
                          (member.id, member.display_name, 0))
                members_added += 1
            except sqlite3.IntegrityError:
                pass
        printc(f'[ ! ]: MEMBERS ADDED TO DATABASE: {members_added}')
        self.conn.commit()
        self.conn.close()

    @comms.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Messages the owner when removed from a guild """
        try:
            # await guild.owner.send(content=f'Goodbye, human', file=discord.File(path('Xiux', 'misc', 'images', 'removed.jpg')))
            pass
        except discord.errors.Forbidden:
            pass
        printc(f'WARNING: CLIENT HAS BEEN REMOVED FROM GUILD {guild}')

    @comms.Cog.listener()
    async def on_member_join(self, member):
        """ Welcome the new member to the guild """
        pass
        # role = discord.utils.get(member.guild.roles, name='Human')
        # await member.add_roles(role)

    @comms.Cog.listener()
    async def on_member_ban(self, guild, user):
        """ """
        print(f'WARNING: {user.name} WAS BANNED FROM {guild.name}')
        try:
            # await user.send(content=f'You have been banned from the server {guild.name}', file=discord.File(path('Xiux', 'misc', 'images', 'removed.jpg')))
            pass
        except discord.errors.Forbidden:
            pass

    @comms.Cog.listener()
    async def on_member_unban(self, guild, user):
        """ """
        pass

    @comms.Cog.listener()
    async def on_member_update(self, before, after):
        """ """
        pass


def setup(bot):
    bot.add_cog(Updates_Cog(bot))
