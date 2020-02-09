"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import asyncio

from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord
from google.cloud import texttospeech

from modules.output import path


class TTS(comms.Cog):
    """Using Google Cloud's Text-To-Speech API to speak through the bot's microphone."""

    def __init__(self, bot):
        self.bot = bot
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('config', 'gsc.json')

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def tts_creation(self):
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(path('tmp', 'tts.mp3'), 'wb') as out:
            out.write(response.audio_content)

    @comms.command()
    @comms.cooldown(60, 60, BucketType.default)
    async def tts(self, ctx, *, message: str):
        vc = ctx.guild.voice_client
        if vc.is_playing():
            await ctx.send('Cannot play anything since some audio is currently running.', delete_after=10)
        await self.bot.loop.run_in_executor(None, self.tts_creation)
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=path('tmp', 'tts.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()


def setup(bot):
    bot.add_cog(TTS(bot))