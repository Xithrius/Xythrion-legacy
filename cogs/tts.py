from discord.ext import commands as comms
from google.cloud import texttospeech  # ssml must be well-formed according to: https://www.w3.org/TR/speech-synthesis/
import discord
import os

from essentials.pathing import path
from essentials.errors import error_prompt


# Error handling for GOOGLE_APPLICATION_CREDENTIALS
try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path('credentials', 'google_service_token.json')
except FileNotFoundError:
    error_prompt('Google service token is not found. Read the README "Help" section to find solutions.')


def googleTTS(string):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=string)
    voice = texttospeech.types.VoiceSelectionParams(language_code='en-AU-Standard-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open(f"{path()}/Voicelines/output.mp3", 'wb') as out:
        out.write(response.audio_content)
    return f"{path()}/Voicelines/output.mp3"


class GoogleCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    @comms.is_owner()
    async def google(self, ctx, option):
        if await ctx.bot.is_owner(ctx.author):
            options = ['say', 'search']
            if option in options:
                if option == 'say':
                    vc = ctx.guild.voice_client
                    if not vc:
                        vc = await ctx.author.voice.channel.connect()
                    tts = ''.join(str(y) for y in (list(ctx.message.content))[12:])
                    googleTTS(tts)
                    vc.play(discord.FFmpegPCMAudio(f"{path()}/Voicelines/output.mp3"))
                    print(f"{ctx.message.author} has said '{tts}' with googleTTS")
                elif option == 'search':
                    pass
            else:
                await ctx.send(f"Option isn't in {', '.join(str(y) for y in options)}")
        else:
            ctx.send(f"{ctx.author.mention}, I do not approve")

    @comms.command()
    @comms.is_owner()
    async def volume(self, ctx, amount):
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = int(amount)
        print(f"{ctx.message.author} has changed the volume to {int(amount)}")


def setup(bot):
    bot.add_cog(GoogleCog(bot))
