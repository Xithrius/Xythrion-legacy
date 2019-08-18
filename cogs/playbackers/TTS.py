"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import asyncio
import aiohttp

from discord.ext import commands as comms
from google.cloud import texttospeech
import discord

from handlers.modules.output import path


class TTS_Playbacker(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('handlers', 'configuration', 'gsc.json')

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def tts(self, ctx):
        """ Text to speech through the bot's mic """
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
            voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)
        except Exception:
            pass
        with open(path('repository', 'tmp', 'output.mp3'), 'wb') as out:
            out.write(response.audio_content)
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=path('repository', 'tmp', 'output.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()


def setup(bot):
    bot.add_cog(TTS_Playbacker(bot))
