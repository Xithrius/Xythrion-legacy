"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import logging

from discord.ext import commands as comms
from discord.ext.commands import Cog, Context

from xythrion.bot import Xythrion


log = logging.getLogger(__name__)


class Warnings(Cog):
    """Warning the user about specific actions taken."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @comms.Cog.listener()
    async def on_command_completion(self, ctx: Context) -> None:
        """Adds a reaction after a command is successfully completed."""
        await ctx.message.add_reaction('\U00002705')

    @comms.Cog.listener()
    async def on_command_error(self, ctx: Context, error: comms.CommandError) -> None:
        """When the command has an error, this event is triggered."""
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        await ctx.message.add_reaction('\U0000274c')

        if isinstance(error, comms.DisabledCommand):
            return await ctx.send('`Command not available.`')

        elif isinstance(error, comms.CommandNotFound):
            return await ctx.send('`Command not found.`')

        elif isinstance(error, comms.UserInputError):
            return await ctx.send(f'`Command raised bad argument: {error}`')

        elif isinstance(error, comms.NotOwner):
            return await ctx.send('`You do not have enough permissions for this command.`')

        elif isinstance(error, comms.CommandOnCooldown):
            return await ctx.send(f'`{error}`')

        elif isinstance(error, comms.CheckFailure):
            return await ctx.send('`You do not have enough permissions to run this command.`')

        elif isinstance(error, comms.MissingPermissions):
            return await ctx.send('`Bot does not have enough permissions for this command.`')

        elif isinstance(error, AssertionError):
            return await ctx.send(f'`Command failed: {error}`')

        else:
            log.debug(f'Error occured: {error}')
