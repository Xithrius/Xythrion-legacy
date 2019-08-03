"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import youtube_dl
import asyncio
import os

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
        self._loop = False

    """ Checking permissions """

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.config['owners']

    """ """

    def cog_unload(self):
        """ """
        try:
            self.vc.stop()
        except AttributeError:
            pass
        for audio in os.listdir(path('repository', 'music')):
            os.remove(path('repository', 'music', audio))

    """ Inputting/outputting YouTube """

    async def dlyt(self, url):
        with youtube_dl.YoutubeDL(self.bot.config['ytdlopts']) as ydl:
            data = ydl.extract_info(url, download=True)
        return data.get("id", None), data.get('title', None)

    async def _play(self, video_id):
        self.vc.play(discord.FFmpegPCMAudio(source=path('repository', 'music', f'{video_id}.mp3'), options='-loglevel fatal'))
        self.vc.source = discord.PCMVolumeTransformer(self.vc.source)
        self.vc.source.volume = 0.2
        while self.vc.is_playing():
            await asyncio.sleep(1)
        self.vc.stop()

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
        await self._play(video_id)
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
    async def volume(self, ctx, volume):
        try:
            volume = int(volume * 100)
            self.vc.source.volume = volume / 100
        except AttributeError:
            await ctx.send("There's no volume to adjust!")


def setup(bot):
    bot.add_cog(Youtube_Playbacker(bot))
