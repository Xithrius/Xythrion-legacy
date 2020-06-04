"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

import discord
from discord.ext import commands as comms

from utils import fancy_embed, markdown_link, tracebacker, wait_for_reaction


class Warnings(comms.Cog):
    """Warning the user about specific actions taken.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot: comms.Bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    async def cog_check(self, ctx: comms.Context) -> bool:
        """Checks if user if owner.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Returns:
            True or false based off of if user is an owner of the bot.

        """
        return await self.bot.is_owner(ctx.author)

    """ Events """

    @comms.Cog.listener()
    async def on_command_completion(self, ctx: comms.Context) -> None:
        """Adds a reaction after a command is successfully completed.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.

        Returns:
            bool: Always None.

        """
        await ctx.message.add_reaction('\U00002705')

    @comms.Cog.listener()
    async def on_command_error(self, ctx: comms.Context, error: comms.CommandError) -> None:
        """When the command has an error, this event is triggered.

        Args:
            ctx (comms.Context): Represents the context in which a command is being invoked under.
            error (comms.CommandError): The error that was raised

        Returns:
            bool: Always None.

        """
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        await ctx.message.add_reaction('\U0000274c')

        if isinstance(error, comms.DisabledCommand):
            return await ctx.send(f'`Command not available.`')

        elif isinstance(error, comms.CommandNotFound):
            return await ctx.send(f'`Command not found.`')

        elif isinstance(error, comms.UserInputError):
            return await ctx.send(f'`Command raised bad argument: {error}`')

        elif isinstance(error, comms.NotOwner):
            return await ctx.send('`You do not have enough permissions for this command.`')

        elif isinstance(error, comms.CommandOnCooldown):
            return await ctx.send(f'`{error}`')

        elif isinstance(error, comms.CheckFailure):
            return await ctx.send(f'`You do not have enough permissions to run this command.`')

        elif isinstance(error, AssertionError):
            return await ctx.send(f'`Command failed: {error}`')

        else:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    '''INSERT INTO FailedCommands(t, id, jump, error) VALUES ($1, $2, $3, $4)''',
                    datetime.now(), ctx.author.id, ctx.message.jump_url, str(error)
                )

            self.bot.log.info(f'Command has thrown error(s). They have been recorded. {error}')
            tracebacker(error)

            await ctx.send(f'`Command has thrown error(s). They have been recorded.`')

    @comms.command()
    async def reports(self, ctx: comms.Context) -> None:
        """ """
        async with self.bot.pool.acquire() as conn:
            r = await conn.fetch('''SELECT * FROM FailedCommands ORDER BY t ASC LIMIT 1''')

            try:
                d = {k: [v] for k, v in r[0].items() if k not in ['id']}

            except IndexError:
                return await ctx.send('`Records show that there are no reports as of now.`')

            d['Time'] = [d.pop('t')[0].strftime('%c')]

            desc = f'{fancy_embed(d, return_str=True)}\n{markdown_link("Jump", d.pop("jump")[0])}'
            embed = discord.Embed(description=desc)

            embed.set_footer(text='Trashcan removes the report from the database.')

            msg = await ctx.send(embed=embed)
            await msg.add_reaction('\U0001f5d1')

            if await wait_for_reaction(ctx, '\U0001f5d1'):
                await conn.execute(
                    '''DELETE FROM FailedCommands WHERE identification = $1''',
                    r[0]['identification']
                )
                await msg.delete()


def setup(bot):
    bot.add_cog(Warnings(bot))
