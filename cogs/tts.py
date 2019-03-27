from discord.ext import commands as comms
from google.cloud import texttospeech  # ssml must be well-formed according to: https://www.w3.org/TR/speech-synthesis/
import discord
import os
import asyncio

from essentials.errors import error_prompt
from essentails.pathing import path


# Error handling for GOOGLE_APPLICATION_CREDENTIALS
try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('credentials', 'google_service_token.json')
except FileNotFoundError:
    error_prompt('Google service token is not found. Read the HELP file section to find solutions.')


class GoogleCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    @comms.is_owner()
    async def tts(self, ctx):
        lock = asyncio.Lock()
        await lock.acquire()
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.types.SynthesisInput(text=''.join(str(y) for y in (list(ctx.message.content))[6:]))
            voice = texttospeech.types.VoiceSelectionParams(language_code='en-AU-Standard-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
            response = client.synthesize_speech(synthesis_input, voice, audio_config)
            with open(path('audio', 'output.mp3'), 'wb') as out:
                out.write(response.audio_content)
        finally:
            vc = ctx.guild.voice_client
            if not vc:
                vc = await ctx.author.voice.channel.connect()
            lock.release()
            await vc.play(discord.FFmpegPCMAudio(path('audio', 'output.mp3')))
        print(f"{ctx.message.author} has said '{''.join(str(y) for y in (list(ctx.message.content))[12:])}' with googleTTS")


def setup(bot):
    bot.add_cog(GoogleCog(bot))


'''
lock = asyncio.Lock()
await lock.acquire()
try:
    downloads = youtubeDownload(url)
finally:
    lock.release()
for i in range(len(downloads)):
    lock = asyncio.Lock()
    await lock.acquire()
    try:
        await ctx.send(f"playing audio #{i + 1}: '{downloads[i]}'")
        vc.play(discord.FFmpegPCMAudio(f'{pathing()}/Music/{downloads[i]}'))
    finally:
        os.remove(f'{pathing()}/Music/{downloads[i]}')
        lock.release()

'''
