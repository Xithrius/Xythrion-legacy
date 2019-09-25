"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import json
import asyncio

from discord.ext import commands as comms
from google.cloud import texttospeech
import discord

from modules.output import path, ds


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('config', 'gsc.json')
with open(path('config', 'config_connections.json')) as f:
    ffmpeg_options = json.load(f)['ytdl']['ffmpeg_options']


class Google_Requester(comms.Cog):
    """Fetching map information from Google."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command(name='tts')
    async def _tts(self, ctx, *, message: str):
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=message)
            voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)
            with open(path('tmp', 'tts.mp3'), 'wb') as out:
                out.write(response.audio_content)
            vc = ctx.guild.voice_client
            if not vc:
                vc = await ctx.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(source=path('tmp', 'tts.mp3'), options='-loglevel fatal'))
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
        except Exception as e:
            await ctx.send(e)
        os.remove(path('tmp', 'tts.mp3'))

    @comms.group()
    async def google(self, ctx):
        """The Google group command.

        Returns:
            The built-in help command if no command is invoked

        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Type the command **;help {ctx.command}** for help')

    @google.command()
    async def youtube(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Google_Requester(bot))
