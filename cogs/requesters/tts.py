"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


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
        self.bot = bot

    async def cog_check(self, ctx):
        """Checks if user if owner.
        
        Returns:
            True or false based off of if user is an owner of the bot.
        
        """
        return await self.bot.is_owner(ctx.author)

    def tts_creation(self, message: str):
        """Creating the audio file for TTS.
        
        Args:
            message (str): The text that will be converted to speech in audio.
        
        """
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=message)
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D', ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(path('tmp', 'tts.mp3'), 'wb') as out:
            out.write(response.audio_content)

    async def tts_status(self, vc, message):
        """Calling tts_creation after joining a channel to play audio.

        Args:
            vc (voice_client): The current voice channel a caller is in.
            message (str): The message to be converted to audio.

        """
        func = functools.partial(self.tts_creation, message)

        await self.bot.loop.run_in_executor(None, func)

        vc.play(discord.FFmpegPCMAudio(source=path('tmp', 'tts.mp3'), options='-loglevel fatal'))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()

    @comms.command(enabled=False)
    async def tts(self, ctx, *, message: str):
        await self.tts_status(ctx.guild.voice_client, message)

    @comms.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Joins and leaves voice channels to announce who has left and who has joined.
        
        Args:
            member (member): The member who had their voice state changed.
            beore (VoiceState): The state of the user before this event was triggered.
            after (VoiceState): The state of the user after this event was triggered.

        """
        """
        async with self.bot.pool.acquire() as conn:
            found = await conn.fetch(
                '''SELECT identification from Punished WHERE identification=$1''',
                member.id)
            if len(found):
                return
        """
        after_ignore = [after.self_mute, after.self_deaf, after.mute, after.deaf, after.self_stream]
        before_ignore = [before.self_mute, before.self_deaf, before.mute, before.deaf, before.self_stream]

        if after_ignore != before_ignore:
            return

        name = member.name if not member.nick else member.nick
        if hasattr(after.channel, 'members'):
            amount = len(after.channel.members)
            vc = after.channel
            if amount >= 2:
                try:
                    await vc.connect()
                except discord.ClientException:
                    pass
            if vc.guild.voice_client and member.id != self.bot.user.id:
                try:
                    await self.tts_status(vc.guild.voice_client, f'{name} joined.')
                except discord.ClientException:
                    pass

        if hasattr(before.channel, 'members'):
            amount = len(before.channel.members)
            if amount == 1 and before.channel.members[0].id == self.bot.user.id:
                await before.channel.guild.voice_client.disconnect()
            else:
                vc = before.channel.guild.voice_client
                if vc:
                    try:
                        await self.tts_status(vc, f'{name} left.')
                    except discord.ClientException:
                        pass

    @comms.command()
    async def join(self, ctx):
        """Joins the channel the caller is currently in."""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention} is not in a voice chat')
        else:
            await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()

    @comms.command()
    async def leave(self, ctx):
        """Leaves voice channel, if the bot is even in one."""
        await ctx.voice_client.disconnect()

    @comms.command()
    async def stop(self, ctx):
        """Stops the current audio stream."""
        ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(TTS(bot))
