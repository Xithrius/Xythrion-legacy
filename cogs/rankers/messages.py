"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sqlite3
import platform

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, printc, now


class Messages_Ranker(comms.Cog):
    """ Leveling up users """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot
        self.db_path = path('repository', 'data', 'user_info.db')

    """ Commands """

    @comms.command(name='rank')
    async def check_COH_rank(self, ctx):
        """ """
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('SELECT id, points FROM Users WHERE id = ?', (ctx.author.id,))
        points = c.fetchall()[0][1]
        embed = discord.Embed(title=f'`Current circle of hell for user {ctx.message.author}`', colour=0xc27c0e, timestamp=now())
        info = f'''
        {ctx.message.author.mention} `stats`:
        `Current circle of hell`: `Level {round((points / 75), 4)}`
        `Total messages sent:` `{points}`
        '''
        embed.add_field(name='`Info`:', value=info)
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='top')
    async def check_top_COH_rank(self, ctx):
        """ """
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('SELECT name, points FROM Users')
        points = sorted(c.fetchall(), lambda x: x[2])
        r = -5
        check = False
        while not check:
            try:
                points = points[:r]
                check = True
            except IndexError:
                r += 1
        embed = discord.Embed(title=f'Top {abs(r)} users', colour=0x27c0e, timestamp=now())
        for i in range(len(points)):
            embed.add_field(name=f'**{points[i][0]}**:', value=f'{points[i][1]} points')
        await ctx.send(embed=embed)

    """ Events """

    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        """ Creating the leveling system for users when joining a guild, and also greeting them """
        printc(f'[WARNING]: CLIENT HAS JOINED GUILD {guild}')
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        try:
            c.execute('''CREATE TABLE Users(
                        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                        name TEXT UNIQUE ON CONFLICT IGNORE,
                        points INTEGER)''')
            self.conn.commit()
        except Exception as e:
            pass
        printc('[...]: SCANNING ALL USERS IN GUILD...')
        members_added = 1
        for member in guild.members:
            try:
                c.execute('''INSERT INTO Users VALUES (?, ?, ?)''', (member.id, member.display_name, 0))
                members_added += 1
            except sqlite3.IntegrityError:
                pass
        printc(f'[ ! ]: MEMBERS ADDED TO DATABASE: {members_added}')
        self.conn.commit()
        self.conn.close()

    @comms.Cog.listener()
    async def on_message(self, message):
        """ Listens for messages to give points in the leveling system """
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('SELECT id, points FROM Users WHERE id = ?', (message.author.id,))
        points = c.fetchall()[0][1]
        c.execute('''UPDATE Users SET points = ? WHERE id = ?''', (points + 1, message.author.id))
        self.conn.commit()


def setup(bot):
    bot.add_cog(Messages_Ranker(bot))
