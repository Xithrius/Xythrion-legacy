'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import asyncio

from discord.ext import commands as comms
import discord
import youtube_dl

from containers.essentials.pathing import path
from containers.playback.youtube_2_mp3 import process_video

# //////////////////////////////////////////////////////////////////////////// #
# Playback cog
# /////////////////////////////////////////////////////////
# All the audio and music needs
# //////////////////////////////////////////////////////////////////////////// #


class PlaybackCog(comms.Cog):

    # //////////////////////// # Object(s): bot
    def __init__(self, bot):
        self.bot = bot

# //////////////////////////////////////////////// # Commands
    # //////////////////////// # Playing audio
    @comms.command()
    @comms.is_owner()
    async def play(self, ctx, url):
        for i in range(len(url)):
            if url[i] == '&':
                url = url[0:i - 1]
                break
        process_video(url, path())
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        await ctx.send(f"playing '{video_title}'")
        vc.play(discord.FFmpegPCMAudio(f'{path()}\\media\\audio\\music\\{video_title}.mp3'))

    # //////////////////////// # Adjusts the volume of the audio
    @comms.command()
    @comms.is_owner()
    async def volume(self, ctx, amount):
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = float(amount)

    # //////////////////////// # Pauses the audio
    @comms.command()
    @comms.is_owner()
    async def pause(self, ctx):
        vc = ctx.guild.voice_client
        vc.pause()

    # //////////////////////// # Resumes the audio
    @comms.command()
    @comms.is_owner()
    async def resume(self, ctx):
        vc = ctx.guild.voice_client
        vc.resume()

    # //////////////////////// # Tells the user what audio is currently playing
    @comms.command()
    @comms.is_owner()
    async def is_playing(self, ctx):
        vc = ctx.guild.voice_client
        vc.is_playing()

    # //////////////////////// # Stops the audio that is playing, if any
    @comms.command()
    @comms.is_owner()
    async def stop(self, ctx):
        vc = ctx.guild.voice_client
        vc.stop()

    # //////////////////////// # Leave the voice channel, if the bot's in one
    @comms.command()
    @comms.is_owner()
    async def leave(self, ctx):
        vc = ctx.guild.voice_client
        await vc.disconnect()

    # //////////////////////// # Join the channel the user is in
    @comms.command()
    @comms.is_owner()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()


def setup(bot):
    bot.add_cog(PlaybackCog(bot))
