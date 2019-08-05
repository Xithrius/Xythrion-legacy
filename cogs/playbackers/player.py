"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import youtube_dl
import json
import os

from discord.ext import commands as comms
import discord

from handlers.modules.output import path

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

with open(path('handlers', 'configuration', 'config.json')) as f:
    info = json.load(f)
ytdl_format_options = info['ytdlopts']
ffmpeg_options = info['ffmpeg_options']
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.2):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.config['owners']

    """ Commands """

    @comms.command()
    async def play(self, ctx, url):
        async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

    @comms.command()
    async def volume(self, ctx, volume: int):
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @comms.command()
    async def leave(self, ctx):
        """ Leave a voice channel """
        await ctx.voice_client.disconnect()

    @comms.command()
    async def pause(self, ctx):
        """ Pauses audio """
        await ctx.guild.voice_client.pause()

    @comms.command()
    async def resume(self, ctx):
        """ Resumes audio """
        await ctx.guild.voice_client.resume()

    @comms.command()
    async def stop(self, ctx):
        """ Discontinues current audio from playing """
        await ctx.voice_client.stop()

    """ Checks """

    @play.before_invoke
    async def ensure_voice(self, ctx):
        """ Makes sure the player is ready before connecting """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention} You are not in a voice chat')
        elif ctx.voice_client.is_playing():
            await ctx.send(f"Stopping Audio to prioritize {ctx.message.author.mention}'s request")
            ctx.voice_client.stop()

    @volume.before_invoke
    @leave.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    async def ensure_voice_modifier(self, ctx):
        """ Checking if the voice client is connected """
        if ctx.voice_client is None:
            await ctx.send(f'Cannot preform the {ctx.command.name} action for a voice chat')


def setup(bot):
    bot.add_cog(Music(bot))
