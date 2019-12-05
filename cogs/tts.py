"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import asyncio
import functools

from discord.ext import commands as comms
from google.cloud import texttospeech
import discord

from modules.output import path


class TTS_Playbacker(comms.Cog):

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

        credentials_path = path('config', 'gsc.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    def create_tts(self, string):
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=string)
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(
            synthesis_input, voice, audio_config)
        return response

    """ Commands """

    @comms.command(enabled=False)
    @comms.is_owner()
    async def tts(self, ctx, *, message: str):
        """ Text to speech through the bot's mic """
        func = functools.partial(self.create_tts, message)
        response = await self.bot.loop.run_in_executor(None, func)
        with open(path('tmp', 'tts.mp3'), 'wb') as out:
            out.write(response.audio_content)
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=path(
            'tmp', 'tts.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()

    @comms.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        return
        # vc = ctx.guild.voice_client
        # vc = ctx.guild.voice_client
        # vc = before.channel.guild.voice_client
        # while vc.is_playing():
        #     await asyncio.sleep(1)
        # vc.stop()
        if before.channel is None:  # User connected
            func = functools.partial(
                self.create_tts, f'{member.name} has connected.')
        elif after.channel is None:  # User disconnected
            func = functools.partial(
                self.create_tts, f'{member.name} has disconnected.')
        elif before.channel.id != after.channel.id:  # User moved channels
            func = functools.partial(
                self.create_tts, f'{member.name} has moved channels.')
        response = await self.bot.loop.run_in_executor(None, func)
        with open(path('tmp', 'vc_change.mp3'), 'wb') as out:
            out.write(response.audio_content)
        # vc.play(discord.FFmpegPCMAudio(source=path(
        #        'tmp', 'vc_change.mp3'), options='-loglevel fatal'))


def setup(bot):
    bot.add_cog(TTS_Playbacker(bot))
