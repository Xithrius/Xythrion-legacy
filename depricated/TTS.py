"""
>> 1Xq4417
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import asyncio

from discord.ext import commands as comms
from google.cloud import texttospeech  # <<< ssml must be well-formed according to: https://www.w3.org/TR/speech-synthesis/
import discord

from Xiux.containers.QOL.pathing import path


# //////////////////////////////////////////////////////////////////////////// #
# Text to speech cog
# //////////////////////////////////////////////////////////////////////////// #
# Using Google Cloud TTS to speak through the bot's mic
# //////////////////////////////////////////////////////////////////////////// #


class TTS_Cog(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """
    Error handling for GOOGLE_APPLICATION_CREDENTIALS
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('Xiux', 'configuration', 'gst.json')
    except FileNotFoundError:
        print('WARNING: GOOGLE SERVICE TOKEN COULD NOT BE FOUND')

    """

    Commands

    """
    @comms.command(name='tts', hidden=True)
    @comms.is_owner()
    async def google_text_to_speech(self, ctx):
        """
        Text to speech through the bot's mic
        """
        lock = asyncio.Lock()
        await lock.acquire()
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
            voice = texttospeech.types.VoiceSelectionParams(language_code='en-AU-Standard-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)
            with open(path('media', 'audio', 'output.mp3'), 'wb') as out:
                out.write(response.audio_content)
        finally:
            lock.release()
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(path('media', 'audio', 'output.mp3')))
        print(f"TTS: {ctx.message.author} said {(ctx.message.content)[5:]}")


def setup(bot):
    bot.add_cog(TTS_Cog(bot))
