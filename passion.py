import discord
import discord.ext.commands as comms

import asyncio

import sqlite3

import os

import datetime
import time

import random

from collections import defaultdict


class PassionBot(comms.Bot):
    def __init__(self, prefix):
        super().__init__([prefix], status=discord.Status.dnd, activity=discord.Game('Logging in . . .'))

        if not os.path.isfile('messages.db'):
            self.initDB()

        self.conn = sqlite3.connect('messages.db')

        self.lastStatus = defaultdict(int)

        self.add_command(self.logoutCommand)
        self.add_command(self.history)
        self.add_command(self.restoreLast)
        self.add_command(self.refreshDB)
        self.add_command(self.imitate)
        self.add_command(self.readHistory)

    @comms.command()
    @comms.is_owner()
    async def readHistory(self, ctx):
        for channel in ctx.guild.text_channels:
            print('READING', channel.id)
            try:
                await self.readChannelHistory(channel)
            except discord.errors.Forbidden:
                pass

    async def readChannelHistory(self, channel):
        c = self.conn.cursor()
        async for message in channel.history(limit=None):
            if not message.author.bot and not self.seenMessage(message.id):
                print('ADDING', message.id)
                c.execute('''INSERT INTO sends VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (message.id,
                           message.author.id,
                           message.channel.id,
                           message.guild.id,
                           int(time.time()),
                           str(message.author),
                           message.content))
        self.conn.commit()

    def chooseRandom(self, dictionary, excludeNone=False):
        dictionary = dict(dictionary.items())
        if excludeNone:
            if None in dictionary:
                del dictionary[None]
        I = random.randrange(sum(dictionary.values()))
        K = None

        for k, v in dictionary.items():
            K = k
            I -= v
            if I <= 0:
                break

        return K

    def seenMessage(self, ID):
        c = self.conn.cursor()
        for r in c.execute('''SELECT * FROM sends WHERE message = ?''', (ID,)):
            return True
        return False

    @comms.command()
    async def imitate(self, ctx, user: comms.MemberConverter, start=None):
        c = self.conn.cursor()

        markov = defaultdict(lambda: defaultdict(int))

        messageAdded = False

        async with ctx.typing():
            for r in c.execute('''SELECT content FROM sends WHERE user = ? AND server = ?''',
                               (user.id, ctx.guild.id)):
                last = None
                if len(r[0]) > 0:
                    messageAdded = True
                    for w in r[0].split(' '):
                        markov[last][w] += 1
                        last = w
                    markov[last][None] += 1

            if not messageAdded:
                await ctx.send(embed=discord.Embed(title=f'Can not imitate {user.display_name}. I need more data.'))
                return

            if start not in markov:
                await ctx.send(embed=discord.Embed(title=f'Can not imitate {user.display_name}. They have never said that. . .'))
                return

            curr = self.chooseRandom(markov[start], start is not None)
            text = ''

            if start is not None:
                text = f' {start}'

            while curr is not None:
                text += f' {curr}'
                curr = self.chooseRandom(markov[curr])

            text = text[1:]

        await ctx.send(embed=discord.Embed(title=f'{user.display_name} sounds like', description=text))

    @comms.command()
    @comms.is_owner()
    async def refreshDB(self, ctx):
        self.conn.close()
        self.conn = sqlite3.connect('messages.db')

    def initDB(self):
        self.conn = sqlite3.connect('messages.db')
        c = self.conn.cursor()
        c.execute('''CREATE TABLE sends (message INTEGER, user INTEGER, channel INTEGER, server INTEGER, timeStamp INTEGER, name TEXT, content TEXT)''')
        c.execute('''CREATE TABLE edits (message INTEGER, user INTEGER, channel INTEGER, server INTEGER, timeStamp INTEGER, name TEXT, before TEXT, after TEXT)''')
        c.execute('''CREATE TABLE deletes (message INTEGER, user INTEGER, channel INTEGER, server INTEGER, timeStamp INTEGER, name TEXT)''')
        c.execute('''CREATE TABLE joinVoice (user INTEGER, timeStamp INTEGER, channel INTEGER)''')
        c.execute('''CREATE TABLE leaveVoice (user INTEGER, timeStamp INTEGER, channel INTEGER)''')
        c.execute('''CREATE TABLE moveVoice (user INTEGER, timeStamp INTEGER, before INTEGER, after INTEGER)''')
        c.execute('''CREATE TABLE voice (user INTEGER, timeStamp INTEGER, muted INTEGER, deafened INTEGER, serverMuted INTEGER, serverDeafened INTEGER)''')
        c.execute('''CREATE TABLE statusChange (user INTEGER, timeStamp INTEGER, status TEXT, game TEXT, nickname TEXT)''')
        self.conn.commit()
        self.conn.close()

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game('Watching you'))

        preStr = ", ".join(map(lambda pre: "\"" + pre + "\"", self.command_prefix))
        ID = (await self.application_info()).id
        centerLines = [f' Logged in as: {self.user} ',
                       f' Client ID: {self.user.id} ',
                       f' Prefixes: {preStr} ',
                       f' Invite URL: {f"https://discordapp.com/oauth2/authorize?client_id={ID}&scope=bot&permissions=2146958839"} ']

        centerLen = max(map(len, centerLines))
        edge = '*' * (max(map(len, centerLines)) + 2)
        print(edge)
        for line in centerLines:
            missing = centerLen - len(line)
            line = ' ' * (missing // 2) + line + ' ' * (missing - missing // 2)

            print(f'*{line}*')
        print(edge)
        print()

    async def logout(self):
        self.conn.close()
        await super().logout()

    @comms.command(name='logout')
    @comms.is_owner()
    async def logoutCommand(self, ctx):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        await self.logout()

    def getHistory(self, messageID):
        c = self.conn.cursor()

        results = []

        for r in c.execute('''SELECT timeStamp, content FROM sends WHERE message = ?''', (messageID,)):
            results.append(r)

        for r in c.execute('''SELECT timeStamp, after FROM edits WHERE message = ?''', (messageID,)):
            results.append(r)

        for r in c.execute('''SELECT timeStamp FROM deletes WHERE message = ?''', (messageID,)):
            results.append((r[0], '***DELETED***'))

        results = sorted(results, key=lambda r: r[0])

        embed = discord.Embed(title=f'Message History ({messageID})')

        for ts, content in results:
            embed.add_field(name=datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p %b %d, %Y'), value=content, inline=False)

        return embed

    @comms.command()
    async def restoreLast(self, ctx, user: comms.MemberConverter):
        c = self.conn.cursor()

        R = None

        for r in c.execute('''SELECT message FROM deletes WHERE timeStamp = (SELECT MAX(timeStamp) FROM deletes) AND user = ?''',
                           (user.id,)):
            R = r[0]

        await ctx.send(embed=self.getHistory(R))

    @comms.command()
    async def history(self, ctx, messageID: int):
        await ctx.send(embed=self.getHistory(messageID))

    async def on_message(self, message):
        if not message.author.bot:
            print('SEND', message.id)
            c = self.conn.cursor()
            c.execute('''INSERT INTO sends VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (message.id,
                       message.author.id,
                       message.channel.id,
                       message.guild.id,
                       int(time.time()),
                       str(message.author),
                       message.content))
            self.conn.commit()

        await super().on_message(message)

    async def on_message_edit(self, before, message):
        if not message.author.bot:
            print('EDIT', message.id)
            c = self.conn.cursor()
            c.execute('''INSERT INTO edits VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (message.id,
                       message.author.id,
                       message.channel.id,
                       message.guild.id,
                       int(time.time()),
                       str(message.author),
                       before.content,
                       message.content))
            self.conn.commit()

    async def on_message_delete(self, message):
        if not message.author.bot:
            print('DELETE', message.id)
            c = self.conn.cursor()
            c.execute('''INSERT INTO deletes VALUES (?, ?, ?, ?, ?, ?)''',
                      (message.id,
                       message.author.id,
                       message.channel.id,
                       message.guild.id,
                       int(time.time()),
                       str(message.author)))
            self.conn.commit()

    async def on_voice_state_update(self, member, before, after):
        print('VOICE', member.id)
        c = self.conn.cursor()
        if before.channel is None:
            c.execute('''INSERT INTO joinVoice VALUES (?, ?, ?);''',
                      (member.id, int(time.time()), after.channel.id))
        elif after.channel is None:
            c.execute('''INSERT INTO leaveVoice VALUES (?, ?, ?);''',
                      (member.id, int(time.time()), before.channel.id))

        elif before.channel.id != after.channel.id:
            c.execute('''INSERT INTO leaveVoice VALUES (?, ?, ?);''',
                      (member.id, int(time.time()), before.channel.id, after.channel.id))

        c.execute('''INSERT INTO voice VALUES (?, ?, ?, ?, ?, ?);''',
                  (member.id, int(time.time()), after.self_mute, after.self_deaf, after.mute, after.deaf))

        self.conn.commit()

    async def on_member_update(self, before, after):
        if before.bot:
            return

        if time.time() - self.lastStatus[after.id] > 1:
            self.lastStatus[after.id] = time.time()
            STATUS = {discord.Status.online: 'online',
                      discord.Status.offline: 'offline',
                      discord.Status.idle: 'idle',
                      discord.Status.dnd: 'dnd'}
            bStatus = STATUS[before.status]
            aStatus = STATUS[after.status]

            bGame = None
            if before.activity is not None:
                bGame = before.activity.name

            aGame = None
            if after.activity is not None:
                aGame = after.activity.name

            bNick = before.display_name
            aNick = after.display_name

            if bStatus != aStatus or bGame != aGame or bNick != aNick:
                print('STATUS', after.id)
                c = self.conn.cursor()
                c.execute('''INSERT INTO statusChange VALUES (?, ?, ?, ?, ?);''',
                          (after.id, int(time.time()), aStatus, aGame, aNick))
                self.conn.commit()

    # async def on_command_completion(self, ctx):
    #     try:
    #         await ctx.message.delete()
    #     except discord.errors.Forbidden:
    #         pass


if __name__ == '__main__':
    bot = PassionBot('p!')

    with open('token.txt', 'r') as f:
        token = f.read()

    bot.run(token)
