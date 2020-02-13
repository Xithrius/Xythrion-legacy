"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import os
import asyncio
import functools

from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
import discord
from google.cloud import texttospeech

from modules import path


class TTS(comms.Cog):
    """Using Google Cloud's Text-To-Speech API to speak through the bot's microphone."""

    def __init__(self, bot):
        """ """
        self.bot = bot

    async def cog_check(self, ctx):
        """ """
        return await self.bot.is_owner(ctx.author)

    def tts_creation(self, message):
        """ """
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=message)
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(path('tmp', 'tts.mp3'), 'wb') as out:
            out.write(response.audio_content)

    @comms.command(enabled=False)
    @comms.cooldown(12, 60, BucketType.default)
    async def tts(self, ctx, *, message: str):
        """ """
        vc = ctx.guild.voice_client
        if vc and vc.is_playing():
            return await ctx.send('`Cannot play anything since some audio is currently running.`')
        if not vc:
            vc = await ctx.author.voice.channel.connect()

        func = functools.partial(self.tts_creation, message)

        await self.bot.loop.run_in_executor(None, func)

        vc.play(discord.FFmpegPCMAudio(source=path('tmp', 'tts.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()

    async def tts_status(self, vc, message):
        func = functools.partial(self.tts_creation, message)

        await self.bot.loop.run_in_executor(None, func)

        vc.play(discord.FFmpegPCMAudio(source=path('tmp', 'tts.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()

    @comms.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Holy MOTHER it finally works."""
        if hasattr(after.channel, 'members'):
            amount = len(after.channel.members)
            vc = after.channel
            if amount >= 2:
                try:
                    await vc.connect()
                except discord.ClientException:
                    pass
            if vc.guild.voice_client and member.id != self.bot.user.id:
                await self.tts_status(vc.guild.voice_client, f'{member.name} has connected.')

        if hasattr(before.channel, 'members'):
            amount = len(before.channel.members)
            if amount == 1 and before.channel.members[0].id == self.bot.user.id:
                await before.channel.guild.voice_client.disconnect()
            else:
                vc = before.channel.guild.voice_client
                if vc:
                    await self.tts_status(vc, f'{member.name} has disconnected.')


    @comms.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(TTS(bot))

"""
        # NOTE: Joining channel
        # NOTE: member.id, int(time.time()), after.channel.id)
        if before.channel is None:
            pass

        # NOTE: Leaving channel
        # NOTE: member.id, int(time.time()), before.channel.id)
        elif after.channel is None:
            pass

        # NOTE: Changing channel
        # NOTE: member.id, int(time.time()), before.channel.id, after.channel.id)
        elif before.channel.id != after.channel.id:
            pass

        # NOTE: Changing voice state
        # NOTE: member.id, int(time.time()), after.self_mute, after.self_deaf, after.mute, after.deaf)
"""
