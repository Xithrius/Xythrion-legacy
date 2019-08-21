"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from discord.ext import commands as comms
import discord


class Interactions_Director(comms.Cog):
    """ Director for interactions """

    def __init__(self, bot):
        """ Object(s):
        Bot
        """
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        return ctx.message.author.id in self.bot.owner_ids

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            pass
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send(f'You do not have enough permissions to run the command **.{ctx.command.name}**')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send(content=f'Command not found, sorry.')

    """ Commands """

    @comms.command(name='join')
    async def _join(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.message.author.mention} You are not in a voice chat')
        else:
            await ctx.author.voice.channel.connect()


def setup(bot):
    bot.add_cog(Interactions_Director(bot))
