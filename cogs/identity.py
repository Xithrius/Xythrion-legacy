'''

+----[ Demonically ]----------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import csv
import datetime
import platform

import discord
from discord.ext import commands as comms

from essentials.pathing import path  # , mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
# Identity cog
# ////////////////////////
# The bot's personal attributes in a cog
# ///////////////////////////////////////////////////////// #


class IdentityCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command(name='owner')
    async def show_creator(self, ctx):
        embed = discord.Embed(colour=0xc27c0e)
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/TtcOXxx.jpg')
        embed.add_field(name='Private Github:', value='[Right here](https://github.com/Xithrius/Demonically)')
        embed.add_field(name='Command caller:', value=ctx.author.mention)
        embed.set_footer(text=f'discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='songs')
    async def favorite_songs(self, ctx):
        embed = discord.Embed(name=f"{self.bot.user}'s favorite songs'", colour=0xc27c0e, timestamp=datetime.datetime.now() + datetime.timedelta(hours=7))
        songs = []
        song_dict = {}
        with open(path('media', 'generated', 'self_generated', 'favorite_songs.csv'), 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                song = row[0]
                artist = row[1]
                song_dict[song] = artist
                songs.append(f"{song} - {artist}")
                try:
                    if ctx.author.activities[0].title == song:
                        if ctx.author.activities[0].artist == artist:
                            embed.add_field(name='A favorite song appears!', value=f"your Spotify is currently playing '{song}' by {artist}, which is one of my favorites!", inline=False)
                except IndexError:
                    pass
        embed.add_field(name='All favorite songs:', value='\n'.join(str(y) for y in songs))
        embed.set_author(name='Xithrius', icon_url='https://i.imgur.com/wzl5IHi.png')
        embed.set_footer(text=f'Python {platform.python_version()} with discord.py rewrite {discord.__version__}', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    @comms.command(name='videos')
    async def favorite_videos(self, ctx):
        pass


def setup(bot):
    bot.add_cog(IdentityCog(bot))
