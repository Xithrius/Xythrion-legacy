"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord

from modules.shortcuts import embed


class Messages_Recorder(comms.Cog):
    """Message count manager"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command()
    async def rank(self, ctx, user: discord.User=False):
        """

        """
        if not user:
            user = ctx.author
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT messages from Messages WHERE identification=$1''',
                user.id)
        e = embed(title=f"{user.name}'s total messages:",
                  desc=f'{info[0]["messages"]}')
        await ctx.send(embed=e)

    """ Events """

    @comms.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            async with self.bot.pool.acquire() as conn:
                info = await conn.fetch(
                 '''SELECT messages FROM Messages WHERE identification=$1''',
                 message.author.id)
                if info:
                    await conn.execute(
                        '''UPDATE Messages SET messages=$2 WHERE
                        identification=$1''',
                        message.author.id, info[0]['messages'] + 1)
                if not info:
                    await conn.execute(
                        '''INSERT INTO Messages(
                            identification, messages) VALUES ($1, $2)''',
                        message.author.id, 1)


def setup(bot):
    bot.add_cog(Messages_Recorder(bot))
