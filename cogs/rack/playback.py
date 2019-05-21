'''
+
|  > Snipped.py
|  > Copyright (c) 2019 Xithrius
|  > MIT license, Refer to LICENSE for more info
+
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


from discord.ext import commands as comms
import discord

from snipped.containers.playback.youtube_2_mp3 import process_video
from snipped.containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Playback cog
# //////////////////////////////////////////////////////////////////////////// #
# All the audio and music needs
# //////////////////////////////////////////////////////////////////////////// #


class PlaybackCog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """

    Commands

    """
    @comms.command()
    @comms.is_owner()
    async def play(self, ctx, url):
        """
        Plays audio from youtube
        """
        for i in range(len(url)):
            if url[i] == '&':
                url = url[0:i]
                break
        video_title = process_video(url, path())
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        await ctx.send(f"`Now playing` **'{video_title}'**")
        vc.play(discord.FFmpegPCMAudio(path('media', 'music', f'{video_title}.mp3')))

    @comms.command()
    @comms.is_owner()
    async def volume(self, ctx, amount):
        """
        Adjusts the volume of the audio
        """
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = float(amount)

    @comms.command()
    @comms.is_owner()
    async def pause(self, ctx):
        """
        Pauses the audio
        """
        vc = ctx.guild.voice_client
        vc.pause()

    @comms.command()
    @comms.is_owner()
    async def resume(self, ctx):
        """
        Resumes the audio
        """
        vc = ctx.guild.voice_client
        vc.resume()

    @comms.command()
    @comms.is_owner()
    async def is_playing(self, ctx):
        """
        Tells the user what audio is currently playing
        """
        vc = ctx.guild.voice_client
        vc.is_playing()

    @comms.command()
    @comms.is_owner()
    async def stop(self, ctx):
        """
        Stops the audio that is playing, if any
        """
        vc = ctx.guild.voice_client
        vc.stop()

    @comms.command()
    @comms.is_owner()
    async def leave(self, ctx):
        """
        Leave the voice channel, if the bot's in one
        """
        vc = ctx.guild.voice_client
        await vc.disconnect()

    @comms.command()
    @comms.is_owner()
    async def join(self, ctx):
        """
        Join the channel the user is in
        """
        try:
            vc = ctx.guild.voice_client
            if not vc:
                await ctx.author.voice.channel.connect()
            if vc.channel != ctx.author.voice.channel:
                await vc.disconnect()
                await ctx.author.voice.channel.connect()
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(PlaybackCog(bot))
