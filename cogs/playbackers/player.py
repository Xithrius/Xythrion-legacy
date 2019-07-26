"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import youtube_dl
import asyncio
import os
import traceback

from discord.ext import commands as comms
import discord

from handlers.modules.output import path, printc, now


class Youtube_Playbacker(comms.Cog):
    """ Playbacker for youtube """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Downloading youtube information """

    async def dlyt(self, url):
        with youtube_dl.YoutubeDL(self.bot.config['ytdlopts']) as ydl:
            data = ydl.extract_info(url, download=True)
            video_id = data.get("id", None)
            video_title = data.get('title', None)
        return video_id, video_title

    """ Commands """

    @comms.command()
    async def play(self, ctx):
        """ """
        url = ctx.message.content[6:]
        data = await self.dlyt(url)
        video_id, video_title = data[0], data[1]
        self.vc = ctx.guild.voice_client
        if not self.vc:
            self.vc = await ctx.author.voice.channel.connect()
        self.vc.play(discord.FFmpegPCMAudio(source=path('repository', 'music', f'{video_id}.mp3'), options='-loglevel fatal'))
        self.vc.source = discord.PCMVolumeTransformer(self.vc.source)
        self.vc.source.volume = 0.05
        while self.vc.is_playing():
            await asyncio.sleep(1)
        self.vc.stop()
        os.remove(path('repository', 'music', f'{video_id}.mp3'))

    @comms.command()
    async def pause(self, ctx):
        """ """
        try:
            self.vc.pause()
        except AttributeError:
            await ctx.send("There's nothing to pause!")

    @comms.command()
    async def resume(self, ctx):
        try:
            self.vc.resume()
        except AttributeError:
            await ctx.send("There's nothing to resume!")

    @comms.command()
    async def stop(self, ctx):
        try:
            self.vc.stop()
        except AttributeError:
            await ctx.send("There's nothing to stop!")

    @comms.command()
    async def volume(self, ctx, volume: int):
        try:
            self.vc.source.volume = volume
        except AttributeError:
            await ctx.send("There's no volume to adjust!")

def setup(bot):
    bot.add_cog(Youtube_Playbacker(bot))
