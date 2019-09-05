"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * I think everything's done here.

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

with open(path('handlers', 'configuration', 'streamer.json')) as f:
    info = json.load(f)
ytdl_format_options = info['ytdlopts']
ffmpeg_options = info['ffmpeg_options']
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    """Creating player to stream audio from YouTube through bot's mic"""

    def __init__(self, source, *, data, volume=0.3):

        #: Subclassing the transformer for streaming.
        super().__init__(source, volume)

        #: YouTube video JSON data as python dictionary
        self.data = data

        #: Getting video information from extracted data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        """Setting up player and data from Youtube url.

        Args:
            url (str): YouTube video url for extracting information and audio stream
            loop (bool): If there's a different loop to check on the player, it is passed.

        """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        #: Returning the source for the player
        return cls(discord.FFmpegPCMAudio(source=data['url'], before_options=ffmpeg_options['options']), data=data)


class Player_Playbacker(comms.Cog):
    """Cog for commands dealing with the YTDLSource subclass."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """Checks user permissions from config file.

        Args:
            ctx: Context object where the command is called.

        Returns:
            True if user has permissions, False otherwise.

        """
        return ctx.message.author.id in self.bot.owner_ids

    """ Commands """

    @comms.command()
    async def play(self, ctx, url):
        """Plays music from YouTube url

        Args:
            ctx: Context object where the command is called.

        Returns:
            Audio stream through the bot's microphone if everything worked out.

        """
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

    @comms.command()
    async def volume(self, ctx, volume: int):
        """Adjusting audio stream volume

        Args:
            ctx: Context object where the command is called.
            volume (int): % volume that bot is to be set at

        Returns:
            A different volume level

        """
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @comms.command()
    async def leave(self, ctx):
        """Leaves voice channel, if the bot is even in one.

        Args:
            ctx: Context object where the command is called.

        Returns:
            It does not return, it leaves from the voice channel.

        """
        await ctx.voice_client.disconnect()

    @comms.command()
    async def pause(self, ctx):
        """Pauses possible audio stream

        Args:
            ctx: Context object where the command is called.

        Returns:
            A paused state of the player.

        """
        ctx.guild.voice_client.pause()

    @comms.command()
    async def resume(self, ctx):
        """Resumes possible audio stream

        Args:
            ctx: Context object where the command is called.

        Returns:
            A resumed state of the player.

        """
        ctx.guild.voice_client.resume()

    @comms.command()
    async def stop(self, ctx):
        """Stops the current audio stream from continuing until another one is requested

        Args:
            ctx: Context object where the command is called.

        Returns:
            A stopped audio stream.

        """
        ctx.voice_client.stop()

    @comms.command(name='join')
    async def _join(self, ctx):
        """Joins the channel the caller is currently in.

        Args:
            ctx: Context object where the command is called.

        Returns:
            This bot within your voice channel.

        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention} You are not in a voice chat')
        else:
            await ctx.author.voice.channel.connect()

    """ Checks """

    @play.before_invoke
    async def ensure_voice(self, ctx):
        """Makes sure the player is ready before connecting to the voice channel

        Args:
            ctx: Context object where the command is called.

        Returns:
            Join if the bot isn't in the caller's voice channel, and/or audio stream when in the voice channel.

        """
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
        """Checking if the voice client is connected.

        Args:
            ctx: Context object where the command is called.

        Returns:
            A bot that is now in the voice channel that the caller is in. There is no escape.

        """
        if ctx.voice_client is None:
            await ctx.send(f'Cannot preform the {ctx.command.name} action for a voice chat')


def setup(bot):
    bot.add_cog(Player_Playbacker(bot))
