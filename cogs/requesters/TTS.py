"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    Stream the voice

"""


import os
import asyncio
import aiohttp

from discord.ext import commands as comms
from google.cloud import texttospeech
import discord

from modules.output import path


class TTS_Playbacker(comms.Cog):
    """Using Google Cloud's Text-To-Speech API to speak through the bot's microphone."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

        #: Setting the environment path so the credentials can be reached by the API.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('config', 'gsc.json')

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.author.id in self.bot.owner_ids

    """ Commands """

    @comms.command()
    async def tts(self, ctx):
        """Text to speech through the bot's microphone.

        Args:
            ctx: Context object where the command is called.
            content (isn't passed into the function): message content that occurs after the command call. Ex. `.tts some string`

        Returns:
            Live text to speech through the bot's mic after downloading the audio, then removing it after.

        """
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
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


def setup(bot):
    bot.add_cog(TTS_Playbacker(bot))
