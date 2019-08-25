"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info

Todo:
    * More interactions to come in the future.
"""


from discord.ext import commands as comms
import discord


class Interactions_Director(comms.Cog):
    """Special interactions between the bot and users"""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Permission checking """

    async def cog_check(self, ctx):
        """Checks user permissions from config file.

        Args:
            ctx: Context object where the command is called.

        Returns:
            True if user has permissions, False otherwise.

        """
        return ctx.message.author.id in self.bot.owner_ids

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a custom message depending on the error.

        Args:
            ctx: Context object where the command is called.
            error: Error object that the command caused.

        Returns:
            A different string depending on the instance of the error

        """
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            pass
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send(f'You do not have enough permissions to run the command **.{ctx.command.name}**')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send(content=f'Command not found, sorry.')


def setup(bot):
    bot.add_cog(Interactions_Director(bot))
