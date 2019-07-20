"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sqlite3
import platform
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, printc, now


class Messages_Ranker(comms.Cog):
    """ Leveling up users """

    def __init__(self, bot):
        """ Object(s):
        Bot
        Path to database
        Checking if a database exists on startup
        Connecting to the database
        Refreshing database background task
        """
        self.bot = bot
        self.db_path = path('repository', 'data', 'user_info.db')
        if not os.path.isfile(self.db_path):
            self.createDB()
        self.conn = sqlite3.connect(self.db_path)
        # self.background_service = self.bot.loop.create_task(self.refreshDB())

    """ Database checking """

    def createDB(self):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE Users(id INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT UNIQUE ON CONFLICT IGNORE, points INTEGER)''')
        self.conn.commit()
        self.conn.close()

    def insertToDB(self, member):
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        c.execute('''INSERT INTO Users VALUES (?, ?, ?)''', (member.id, member.display_name, 1))
        self.conn.commit()

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
        points = c.fetchall()
        points = sorted(points, key=lambda x: x[1], reverse=True)
        if len(points) > 5:
            points = points[:-5]
        longestName = max(map(len, [x[0] for x in points]))
        longestPoint = max(map(len, [str(round((x[1] / 75), 4)) for x in points]))
        points = [f'[{x[0].rjust(longestName)}] : {str(round((x[1] / 75), 4)).rjust(longestPoint)} : ({x[1]})' for x in points]
        points = '\n'.join(str(y) for y in points)
        title = f'[{"Name".rjust(longestName)}] : [{"Circle".rjust(longestPoint)}] [(Messages sent)]'
        info = f'''```css\n{title}\n{points}```'''
        await ctx.send(f'__**Top 5 users in the circles of hell**__:{info}')
        self.conn.close()

    """ Events """

    @comms.Cog.listener()
    async def on_guild_join(self, guild):
        """ Creating the leveling system for users when joining a guild, and also greeting them """
        printc(f'[WARNING]: CLIENT HAS JOINED GUILD {guild}')
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
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

    @comms.Cog.listener()
    async def on_message(self, message):
        """ Listens for messages to give points in the leveling system """
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()
        try:
            c.execute('SELECT id, points FROM Users WHERE id = ?', (message.author.id,))
            points = c.fetchall()[0][1]
            c.execute('''UPDATE Users SET points = ? WHERE id = ?''', (points + 1, message.author.id))
            self.conn.commit()
            if points % 75 == 0:
                embed = discord.Embed(title=f'#({points / 75}) circle of Hell reached', colour=0xc27c0e, timestamp=now())
                embed.add_field(name=f'Total messages sent by {message.author.user}', value=f'{points} messages')
                await message.channel.send(embed=embed)
        except IndexError:
            self.insertToDB(message.author)
            self.conn.close()


def setup(bot):
    bot.add_cog(Messages_Ranker(bot))
