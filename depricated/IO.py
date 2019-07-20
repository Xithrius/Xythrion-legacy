"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import platform
import json
import os
import datetime
import random

from discord.ext import commands as comms
import discord

from Xiux.containers.QOL.shortened import now
from Xiux.containers.QOL.pathing import path, create_dir
from Xiux.containers.output.printer import printc


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
        if ctx.invoked_subcommand is None:
            try:
                with open(path('repository', 'seen', ctx.message.author, 'seen.txt'), 'r') as f:
                    not_seen = True
                    while not_seen:
                        chosen_user = random.choice(os.listdir(path('repository', 'memes')))
                        chosen_meme = random.choice(os.listdir(path('repository', 'memes', chosen_user)))
                        if [chosen_user, chosen_meme] in [x.split('~~') for x in f]:
                            pass
            except FileNotFoundError:
                pass
            info = f'''
            **Info**:
            `Uploader`: {chosen_user}
            `Upload date`: {datetime.datetime.fromtimestamp(int(chosen_meme))}
            `Upvotes`: {json.load(open(path('repository', 'memes', chosen_user, chosen_meme, 'info.json')))['upvotes']}
            '''
            embed = discord.Embed(title=info, colour=0xc27c0e, timestamp=now())
            await ctx.send(embed=embed, file=discord.File(path('repository', 'memes', chosen_user, chosen_meme, 'image.png')))
            os.makedirs(path('repository', 'seen', ctx.message.author))
            with open(path('repository', 'seen', ctx.message.author, 'seen.txt'), 'a') as f:
                f.write(f'{ctx.message.author}~~{chosen_meme}')

    @meme.command()
    async def help(self, ctx):
            """
            Gives the user information on how the meme input/output works
            """
            embed = discord.Embed(title='Help for the meme command', colour=0xc27c0e, timestamp=now())
            help = '''
            `$meme`
            `Gives a meme from the repository. User must have uploaded 5 memes to get theirs seen.`
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
                    await message.channel.send('Meme successfully uploaded')
            except (IndexError, AttributeError):
                pass
            except FileExistsError:
                await message.channel.send('Please wait 1 or more seconds until uploading another meme')


def setup(bot):
    bot.add_cog(IO_Requester(bot))
