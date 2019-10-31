"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime
import sys
import traceback

from discord.ext import commands as comms
import discord

from modules.output import cs, get_extensions


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

    """ Commands """

    @comms.command(aliases=['refresh', 'r'])
    async def reload(self, ctx):
        """Finds all cogs within the 'cogs' directory then loads/unloads them.

        Returns:
            Success or faliure message depending on extension loading

        """
        broken_extensions = []
        for ext in get_extensions():
            try:
                self.bot.unload_extension(ext)
                self.bot.load_extension(ext)
            except discord.ext.commands.ExtensionNotLoaded:
                self.bot.load_extension(ext)
            except Exception as e:
                broken_extensions.append(f'{ext} - {e}')
        if broken_extensions:
            info = '\n'.join(y for y in broken_extensions)
            await ctx.send(f'```\n{info}```', delete_after=15)
        else:
            await ctx.send('Reloaded all extensions.', delete_after=5)

    @comms.command(aliases=['disconnect', 'dc'])
    async def exit(self, ctx):
        """Logs out the bot.

        Returns:
            A possible timeout error.

        """
        await self.bot.conn.execute('''INSERT INTO Runtime
                                    (login, logout) VALUES($1, $2)''',
                                    self.bot.login_time,
                                    datetime.datetime.now())
        cs.w('Logging out...')
        await ctx.bot.logout()

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
