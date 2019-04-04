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


import asyncio

import discord
from discord.ext import commands as comms
import youtube_dl

from essentials.pathing import path, mkdir
# from essentials.errors import error_prompt, input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


class PlaybackCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands
    @comms.command()
    @comms.is_owner()
    async def play(self, ctx, url):
        lock = asyncio.Lock()
        await lock.acquire()
        try:
            mkdir('audio', 'music')
            ydl_opts = {
                'outtmpl': f'{path()}/audio/music/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '200',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', None)
        finally:
            lock.release()
            vc = ctx.guild.voice_client
            if not vc:
                vc = await ctx.author.voice.channel.connect()
            await ctx.send(f"playing '{video_title}'")
            vc.play(discord.FFmpegPCMAudio(f'{path()}/audio/music/{video_title}.mp3'))

    @comms.command(name='s2y')
    @comms.is_owner()
    async def spotify_to_youtube(self, ctx):
        pass

    @comms.command()
    @comms.is_owner()
    async def volume(self, ctx, amount):
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = float(amount)

    @comms.command()
    @comms.is_owner()
    async def pause(self, ctx):
        vc = ctx.guild.voice_client
        vc.pause()

    @comms.command()
    @comms.is_owner()
    async def resume(self, ctx):
        vc = ctx.guild.voice_client
        vc.resume()

    @comms.command()
    @comms.is_owner()
    async def is_playing(self, ctx):
        vc = ctx.guild.voice_client
        vc.is_playing()

    @comms.command()
    @comms.is_owner()
    async def stop(self, ctx):
        vc = ctx.guild.voice_client
        vc.stop()

    @comms.command()
    @comms.is_owner()
    async def leave(self, ctx):
        vc = ctx.guild.voice_client
        await vc.disconnect()

    @comms.command()
    @comms.is_owner()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()


def setup(bot):
    bot.add_cog(PlaybackCog(bot))
