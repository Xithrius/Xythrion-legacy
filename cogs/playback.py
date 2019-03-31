#!/usr/bin/env python


'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

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
