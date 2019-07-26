"""
>> 1Xq4417
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

        credentials_path = path('handlers', 'configuration', 'google_service_credentials.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    """ Commands """

    @comms.command()
    @comms.is_owner()
    async def tts(self, ctx):
        """ Text to speech through the bot's mic """
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
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

    @comms.command(hidden=True)
    @comms.is_owner()
    async def test_tts(self, ctx):
        """ TTS through the REST API """
        url = 'https://texttospeech.googleapis.com/v1beta1/text:synthesize'
        # data = self.bot.config['google']
        # data['text'] = ctx.message.content[5:]
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.tts) as response:
                await ctx.send(response.status)
                await ctx.send(response)
                if response.status == 200:
                    js = await response.json()


def setup(bot):
    bot.add_cog(TTS_Playbacker(bot))
