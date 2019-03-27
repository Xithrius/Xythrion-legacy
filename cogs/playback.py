from discord.ext import commands as comms
import discord


class PlaybackCog(comms.Cog):

    def __init__(self, bot):
        self.bot = bot

    @comms.command()
    @comms.is_owner()
    async def volume(self, ctx, amount):
        vc = ctx.guild.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = int(amount)
        print(f"{ctx.message.author} has changed the volume to {int(amount)}")

    @comms.command()
    @comms.is_owner()
    async def pause(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            vc = ctx.guild.voice_client
            vc.pause()
        else:
            await ctx.send(f"{ctx.author.mention} you can't do this")

    @comms.command()
    @comms.is_owner()
    async def resume(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            vc = ctx.guild.voice_client
            vc.resume()
        else:
            await ctx.send(f"{ctx.author.mention} you can't do this")

    @comms.command()
    @comms.is_owner()
    async def is_playing(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            vc = ctx.guild.voice_client
            vc.is_playing()
        else:
            await ctx.send(f"{ctx.author.mention} you can't do this")

    @comms.command()
    @comms.is_owner()
    async def stop(self, ctx):
        if await ctx.bot.is_owner(ctx.author):
            vc = ctx.guild.voice_client
            vc.stop()
        else:
            await ctx.send(f"{ctx.author.mention} you can't do this")

    @comms.command()
    @comms.is_owner()
    async def leave(self, ctx):
        vc = ctx.guild.voice_client
        await vc.disconnect()

    @comms.command()
    @comms.is_owner()
    async def join(self, ctx):
        await ctx.author.voice.channel.connect()


def setup(bot):
    bot.add_cog(PlaybackCog(bot))
