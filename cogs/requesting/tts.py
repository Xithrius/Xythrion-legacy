"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncio
import functools

import discord
from discord.ext import commands as comms
from discord.ext.commands.cooldowns import BucketType
from google.cloud import texttospeech
from hyper_status import Status

from modules import path


class TTS(comms.Cog):
    """Using Google Cloud's Text-To-Speech API to speak through the bot's microphone.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    """ Cog-specific checks """

    async def cog_check(self, ctx):
        """Checks if user if owner.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    """ Cog-specific functions """

    def tts_creation(self, message: str):
        """Creating the audio file for TTS.

        Args:
            message (str): The text that will be converted to speech in audio.

        """
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=message)
        voice = texttospeech.types.VoiceSelectionParams(language_code='en-US-Wavenet-D',
                                                        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
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

    """ Events """

    @comms.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Joins and leaves voice channels to announce who has left and who has joined.

        Args:
            member (member): The member who had their voice state changed.
            beore (VoiceState): The state of the user before this event was triggered.
            after (VoiceState): The state of the user after this event was triggered.

        """
        return
        after_ignore = [
            after.deaf, after.mute, after.self_mute, after.self_deaf,
            after.self_stream, after.self_video, after.afk
        ]
        before_ignore = [
            before.deaf, before.mute, before.self_mute, before.self_deaf,
            before.self_stream, before.self_video, before.afk
        ]

        if after_ignore != before_ignore:
            return

        # Removed temporarily until records are up. This function was abused way too much.
        # name = member.name if not member.nick else member.nick
        name = member.name
        if hasattr(after.channel, 'members'):
            amount = len(after.channel.members)
            vc = after.channel
            if amount >= 2:
                try:
                    await vc.connect()
                except discord.ClientException:
                    pass
                except asyncio.exceptions.TimeoutError:
                    Status(f'Voice channel {vc} timed out while connecting.', 'fail')
            if vc.guild.voice_client and member.id != self.bot.user.id:
                try:
                    await self.tts_status(vc.guild.voice_client, f'{name} joined.')
                except discord.ClientException:
                    pass

        elif hasattr(before.channel, 'members'):
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

    """ Commands """

    @comms.command()
    @comms.cooldown(1, 8, BucketType.guild)
    async def join(self, ctx):
        """Joins the channel the caller is currently in.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]join

        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention} is not in a voice chat')
        else:
            await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()

    @comms.command()
    @comms.cooldown(1, 8, BucketType.guild)
    async def leave(self, ctx):
        """Leaves voice channel, if the bot is even in one.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]leave

        """
        await ctx.voice_client.disconnect()

    @comms.command()
    @comms.cooldown(1, 8, BucketType.guild)
    async def stop(self, ctx):
        """Stops the current audio stream.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]stop

        """
        ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(TTS(bot))
