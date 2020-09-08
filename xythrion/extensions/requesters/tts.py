import asyncio
import logging
from pathlib import Path

from discord import ClientException, FFmpegPCMAudio, Member, PCMVolumeTransformer, VoiceState
from discord.ext.commands import Cog, Context, command
from gtts import gTTS

from xythrion.utils import DefaultEmbed

log = logging.getLogger(__name__)


class TTS(Cog):
    """Using Google Cloud's Text-To-Speech API to speak."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        """Checking if the user running commands is the owner of this bot."""
        return await self.bot.is_owner(ctx.author)

    @staticmethod
    def tts_creation(message: str) -> None:
        """Creating the audio file for TTS."""
        tts = gTTS(message)
        tts.save(str(Path.cwd() / 'tmp' / 'tts.mp3'))

    async def speak_message(self, vc, message) -> None:
        """Calling tts_creation after joining a channel to play audio."""
        await self.bot.loop.run_in_executor(None, self.tts_creation, message)

        vc.play(FFmpegPCMAudio(source=Path.cwd() / 'tmp' / 'tts.mp3', options='-loglevel fatal'))
        vc.source = PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

        while vc.is_playing():
            await asyncio.sleep(1)

        vc.stop()

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        """Joins and leaves voice channels to announce who has left and who has joined."""
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

        name = member.name
        if hasattr(after.channel, 'members'):
            amount = len(after.channel.members)
            vc = after.channel
            if amount >= 2:
                try:
                    await vc.connect()

                except ClientException:
                    pass

                except asyncio.exceptions.TimeoutError:
                    log.warning(f'Voice channel {vc} timed out while connecting.')

            if vc.guild.voice_client and member.id != self.bot.user.id:
                try:
                    await self.speak_message(vc.guild.voice_client, f'{name} joined.')
                except ClientException:
                    pass

        elif hasattr(before.channel, 'members'):
            amount = len(before.channel.members)
            if amount == 1 and before.channel.members[0].id == self.bot.user.id:
                await before.channel.guild.voice_client.disconnect()
            else:
                vc = before.channel.guild.voice_client
                if vc:
                    try:
                        await self.speak_message(vc, f'{name} left.')
                    except ClientException:
                        pass

    @command(name='tts', hidden=True)
    async def message_to_speech(self, ctx: Context, *, msg: str) -> None:
        await self.speak_message(ctx.voice_client, msg)

    @command()
    async def join(self, ctx: Context) -> None:
        """Joins the channel the caller is currently in."""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()

            else:
                embed = DefaultEmbed(description=f'{ctx.message.author.name} is not in a voice chat')
                await ctx.send(embed=embed)

        else:
            await ctx.voice_client.disconnect()
            await ctx.author.voice.channel.connect()

    @command()
    async def leave(self, ctx: Context) -> None:
        """Leaves voice channel, if the bot is even in one."""
        await ctx.voice_client.disconnect()
