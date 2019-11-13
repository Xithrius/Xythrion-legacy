"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import traceback

from discord.ext import commands as comms

from modules.output import cs


class Warnings_Director(comms.Cog):
    """ """

    def __init__(self, bot):

        #: Setting Xythrion(comms.Bot) as a class attribute
        self.bot = bot

    """ Checks """

    async def cog_check(self, ctx):
        """Checks if the command caller is an owner.

        Returns:
            True or false, depending on if the user is an owner.

        """
        return await self.bot.is_owner(ctx.author)

    """ Events """

    @comms.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Catches errors caused by users

        Returns:
            An error message only if the error is caused by a user.

        Raises:
            A traceback message if there's an internal error.

        """
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, comms.DisabledCommand):
            return await ctx.send(
                cs.css(f'Command {ctx.command} not available.'))

        elif isinstance(error, comms.CommandNotFound):
            return await ctx.send(
                cs.css(f'Command {ctx.command} not found.'))

        elif isinstance(error, comms.UserInputError):
            return await ctx.send(
                cs.css(f'Command {ctx.command} raised bad argument: {error}'))

        elif isinstance(error, comms.NotOwner):
            return await ctx.send(
                cs.css('You do not have enough permissions for this command.'))

        else:
            print(f'Ignoring exception in command {ctx.command}:',
                  file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(Warnings_Director(bot))
