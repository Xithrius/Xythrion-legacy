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
import json
import os
import datetime
import random

from discord.ext import commands as comms
import discord

from rehasher.containers.QOL.shortened import now
from rehasher.containers.QOL.pathing import path, create_dir
from rehasher.containers.output.printer import printc


# //////////////////////////////////////////////////////////////////////////// #
# Input/request cog
# //////////////////////////////////////////////////////////////////////////// #
# Get information from other user's input
# //////////////////////////////////////////////////////////////////////////// #


class IO_Requester(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.group()
    async def meme(self, ctx):
        """
        Gives a random meme from the repository of memes
        """
        chosen_user = random.choice(os.listdir(path('repository', 'memes')))
        chosen_meme = random.choice(os.listdir(path('repository', 'memes', chosen_user)))
        embed = discord.Embed(title=f'`Uploader`: {chosen_user}', colour=0xc27c0e, timestamp=now())
        info = f'''
        `Upload date`: {datetime.datetime.fromtimestamp(int(chosen_meme))}
        `Upvotes`: {json.load(open(path('repository', 'memes', chosen_user, chosen_meme, 'info.json')))['upvotes']}
        '''
        embed.add_field(name='**Info**:', value=info)
        await ctx.send(embed=embed, file=discord.File(path('repository', 'memes', chosen_user, chosen_meme, 'image.png')))

    @meme.command()
    async def help(self, ctx):
            """
            Gives the user information on how the meme input/output works
            """
            embed = discord.Embed(title='', colour=0xc27c0e, timestamp=now())
            help = '''
            `$ <> <>`
            `<>`: ``
            `<>`: ``
            '''
            embed.add_field(name='Usage:', value=help)
            embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
            await ctx.send(embed=embed)

    """

    Events

    """
    @comms.Cog.listener()
    async def on_message(self, message):
        if str(message.author) != str(self.bot.user):
            try:
                if (any(i in message.attachments[0].filename for i in ['.jpg', '.png', '.jpeg'])) and (not message.guild):
                    date = (int(datetime.datetime.timestamp(datetime.datetime.now())))
                    os.makedirs(path('repository', 'memes', message.author, date))
                    with open(path('repository', 'memes', message.author, date, 'info.json'), 'w') as f:
                        info = {'user': str(message.author), 'upvotes': 0}
                        json.dump(info, f)
                    await message.attachments[0].save(path('repository', 'memes', message.author, date, 'image.png'))
            except (IndexError, AttributeError):
                pass


def setup(bot):
    bot.add_cog(IO_Requester(bot))
