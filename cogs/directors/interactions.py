"""
>> 1Xq4417
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
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            pass
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send(f'You do not have enough permissions to run the command **.{ctx.command.name}**')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            msg = ctx.message.content
            try:
                msg = msg[:msg.index(' ')]
            except ValueError:
                pass
            possibilities = [x.name for x in self.bot.commands]
            if len(possibilities):
                embed = discord.Embed(title='\n'.join(str(y) for y in [x.name for x in self.bot.commands] if y in msg))
                await ctx.send(content=f'**{msg}** command not found. Maybe you meant one of the following?', embed=embed)
            else:
                await ctx.send(f'Could not find a command similar to **{msg}**')
        else:
            await ctx.send(f'Notifying owner <@{self.bot.owner_id}> of error `{error}`')


def setup(bot):
    bot.add_cog(Interactions_Director(bot))
