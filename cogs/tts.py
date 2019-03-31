'''

MIT License

Copyright (c) 2019 Xithrius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


# ///////////////////////////////////////////////////////// #
# authorship information
# ////////////////////////
# Description of the author(s) information
# ///////////////////////////////////////////////////////// #


__author__ = 'Xithrius'

__copyright__ = 'MIT License, Copyright (c) 2019 Xithrius'

__credits__ = ["Xithrius", "Rapptz"]
# Xithrius : Project owner
# Rapptz   : Discord.py API wrapper creator

__license__ = "MIT"

__version__ = "0.00.0009"

__maintainer__ = "Xithrius"

__status__ = "Development"


# ///////////////////////////////////////////////////////// #
# Libraries
# ////////////////////////
# Built-in modules
# Third-party modules
# Custom modules
# ///////////////////////////////////////////////////////// #


import os
import asyncio

import discord
from discord.ext import commands as comms
from google.cloud import texttospeech  # ssml must be well-formed according to: https://www.w3.org/TR/speech-synthesis/

from essentials.pathing import path  # , mkdir
from essentials.errors import error_prompt  # , input_loop
# from essentials.welcome import welcome_prompt


# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


class GoogleCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Error handling for GOOGLE_APPLICATION_CREDENTIALS
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('credentials', 'google_service_token.json')
    except FileNotFoundError:
        error_prompt('Google service token is not found. Read the HELP file section to find solutions.')

    @comms.command(name='tts')
    @comms.is_owner()
    async def google_text_to_speech(self, ctx):
        lock = asyncio.Lock()
        await lock.acquire()
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=(ctx.message.content)[5:])
            voice = texttospeech.types.VoiceSelectionParams(language_code='en-AU-Standard-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)
            with open(path('audio', 'output.mp3'), 'wb') as out:
                out.write(response.audio_content)
        finally:
            lock.release()
        vc = ctx.guild.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(path('audio', 'output.mp3')))
        print(f"TTS: {ctx.message.author} said {(ctx.message.content)[5:]}")


def setup(bot):
    bot.add_cog(GoogleCog(bot))
