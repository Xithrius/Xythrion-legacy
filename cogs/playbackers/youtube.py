"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import youtube_dl
import asyncio

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

    """ Commands """

    @comms.command()
    async def play(self, ctx, url):
        """ """
        async with youtube_dl.YoutubeDL(self.bot.config['ytdlopts']) as ydl:
            ydl.download([url])
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=path('repository', 'tmp', 'music.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()


def setup(bot):
    bot.add_cog(Youtube_Playbacker(bot))
