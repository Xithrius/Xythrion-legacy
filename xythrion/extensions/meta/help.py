import asyncio
import itertools
import typing as t
from collections import namedtuple
from contextlib import suppress

import discord
from discord.ext.commands import Cog, Command, Context, Group, HelpCommand
from fuzzywuzzy import fuzz, process

from xythrion.bot import Xythrion
from xythrion.utils import PaginatedEmbed

COMMANDS_PER_PAGE = 8
DELETE_EMOJI = '❌'

Category = namedtuple('Category', ('name', 'description', 'cogs'))


# Yoinked from: https://github.com/Snek-Network/snek/blob/master/snek/exts/core/help_command.py


async def help_cleanup(bot: Xythrion, author: discord.Member, message: discord.Message) -> None:
    """
    Cleanup the help command.

    Adds the `DELETE_EMOJI` reaction. When clicked, it will delete the help message.
    After a 300 second timeout, the reaction will be removed.
    """

    def check(reaction: discord.Reaction, user: discord.User) -> bool:
        return reaction.message.id == message.id and user.id == author.id and str(reaction) == DELETE_EMOJI

    await message.add_reaction(DELETE_EMOJI)

    with suppress(discord.NotFound):
        try:
            await bot.wait_for('reaction_add', check=check, timeout=300)
        except asyncio.TimeoutError:
            await message.remove_reaction(DELETE_EMOJI, bot.user)
        else:
            await message.delete()


class HelpQueryNotFound(ValueError):
    """
    Raised when a query from the help command doesn't match a command or cog.

    Contains the attribute `possible_matches`, a dictionary of any command(s)
    that were close the matching the query. The keys are possible matched
    command(s) and values are the likeliness scores.
    """

    def __init__(self, arg: str, possible_matches: t.Optional[t.Dict]) -> None:
        super().__init__(arg)
        self.possible_matches = possible_matches


class CustomHelpCommand(HelpCommand):
    """A custom paginated help command."""

    def __init__(self) -> None:
        super().__init__(command_attrs={'help': 'Shows help for bot commands.'})

    async def command_callback(self, ctx: Context, *, command: t.Optional[str] = None) -> None:
        """Attempts to match the query with a valid command or cog."""
        if command is None:
            mapping = self.get_bot_mapping()
            await self.send_bot_help(mapping)
            return

        cog_matches = list()
        description = None

        for cog in ctx.bot.cogs.values():
            if hasattr(cog, 'category') and cog.category == command:
                cog_matches.append(cog)

                if hasattr(cog, 'category_description'):
                    description = cog.category_description

        if cog_matches:
            category = Category(name=command, description=description, cogs=cog_matches)
            await self.send_category_help(category)
            return

        await super().command_callback(ctx, command=command)

    async def get_all_help_choices(self) -> t.Set[str]:
        """
        Get all the options for getting help with the bot.

        This will only display commands the author has permission to use, including:
        - Category names
        - Cog names
        - Group command names
        - Command names
        - Subcommand names
        """
        choices = set()
        for command in await self.filter_commands(self.context.bot.walk_commands()):
            # Command/group name
            choices.add(str(command))

            if isinstance(command, Command):
                # All aliases if it's a command
                choices.update(command.aliases)
            else:
                # Add parent name
                choices.update(f'{command.full_parent_name} {alias}' for alias in command.aliases)

        # Add cog names
        choices.update(self.context.bot.cogs)

        # Add category names
        choices.update(
            cog.category for cog in self.context.bot.cogs.values() if hasattr(cog, 'category')
        )

        return choices

    async def command_not_found(self, string: str) -> HelpQueryNotFound:
        """Handles when a query does not match a valid command, group, cog, or category."""
        choices = await self.get_all_help_choices()
        result = process.extractBests(string, choices, scorer=fuzz.ratio, score_cutoff=60)

        return HelpQueryNotFound(f'Query "{string}" not found.', dict(result))

    async def subcommand_not_found(self, command: Command, string: str) -> HelpQueryNotFound:
        """Redirect to `command_not_found`."""
        return await self.command_not_found(f'{command.qualified_name} {string}')

    async def send_error_message(self, error: HelpQueryNotFound) -> None:
        """Send the error message the the channel."""
        embed = discord.Embed(color=discord.Color.red(), title=str(error))

        if getattr(error, 'possible_matches', None):
            matches = '\n'.join(f'`{match}`' for match in error.possible_matches)
            embed.description = f'**Did you mean:**\n{matches}'

        await self.context.send(embed=embed)

    async def command_formatting(self, command: Command) -> discord.Embed:
        """Turns a command into an embed."""
        embed = discord.Embed()
        embed.set_author(name='Command Help')

        parent = command.full_parent_name
        name = str(command) if not parent else f'{parent} {command.name}'
        prefix = self.context.prefix

        # Show command signature
        command_details = f'**```{prefix}{name} {command.signature}```**\n'

        # Show aliases
        aliases = ', '.join(
            f'`{alias}`' if not parent else f'`{parent} {alias}`'
            for alias in command.aliases
        )
        if aliases:
            command_details += f'**Aliases:** {aliases}\n\n'

        # Check if user is allowed to run this command
        if not await command.can_run(self.context):
            command_details += '***You cannot run this command.***\n\n'

        command_details += f'*{command.help or "No details provided."}*\n'
        embed.description = command_details

        return embed

    async def send_command_help(self, command: Command) -> None:
        """Send help for a single command."""
        embed = await self.command_formatting(command)
        message = await self.context.send(embed=embed)
        await help_cleanup(self.context.bot, self.context.author, message)

    def get_command_details(
            self, commands: t.List[Command], return_as_list: bool = False
    ) -> t.Union[t.List[str], str]:
        """Format the prefix, command name, signature, and short docs."""
        details = list()
        prefix = self.context.prefix

        for command in commands:
            signature = f' {command.signature}' if command.signature else ''
            details.append(
                f'\n**`{prefix}{command.qualified_name}{signature}`**'
                f'\n*{command.short_doc or "No details provided."}*'
            )

        if return_as_list:
            return details

        return ''.join(details)

    async def send_group_help(self, group: Group) -> None:
        """Sends help for a group command."""
        if len(group.commands) == 0:
            # Treat as a regular command if there's no subcommands
            await self.send_command_help(group)
            return

        commands = await self.filter_commands(group.commands, sort=True)
        embed = await self.command_formatting(group)

        command_details = self.get_command_details(commands)
        if command_details:
            embed.description += f'\n**Subcommands:**\n{command_details}'

        message = await self.context.send(embed=embed)
        await help_cleanup(self.context.bot, self.context.author, message)

    async def send_cog_help(self, cog: Cog) -> None:
        """Send help for a cog."""
        commands = await self.filter_commands(cog.get_commands(), sort=True)

        embed = discord.Embed()
        embed.set_author(name='Command Help')
        embed.description = f'**{cog.qualified_name}**\n*{cog.description}*'

        command_details = self.get_command_details(commands)
        if command_details:
            embed.description += f'\n\n**Commands:**\n{command_details}'

        message = await self.context.send(embed=embed)
        await help_cleanup(self.context.bot, self.context.author, message)

    @staticmethod
    def _category_key(command: Command) -> str:
        """
        Returns a cog name of a given command for use as a key for `sorted` and `groupby`.

        A zero width space is used as a prefix for results with no cogs to sort them last.
        """
        if command.cog:
            with suppress(AttributeError):
                if command.cog.category:
                    return f'**{command.cog.category}**'
            return f'**{command.cog_name}**'

        return '**\u200bNo Category:**'

    async def send_category_help(self, category: Category) -> None:
        """Send help for a category."""
        all_commands = list()
        for cog in category.cogs:
            all_commands.extend(cog.get_commands())

        filtered_commands = await self.filter_commands(all_commands, sort=True)

        command_details_list = self.get_command_details(
            filtered_commands,
            return_as_list=True
        )
        description = f'**{category.name}**\n*{category.description}*'

        if command_details_list:
            description += '\n\n**Commands:**'

        category_embed = PaginatedEmbed.from_lines(
            lines=command_details_list,
            prefix=description,
            max_lines=COMMANDS_PER_PAGE,
        )
        category_embed.set_author(name='Command Help')
        await category_embed.paginate(self.context)

    async def send_bot_help(self, mapping: t.Dict) -> None:
        """Send help for all bot commands and cogs."""
        bot = self.context.bot

        filter_commands = await self.filter_commands(
            bot.commands,
            sort=True,
            key=self._category_key
        )

        cog_or_category_pages = list()

        grouped_commands = itertools.groupby(filter_commands, key=self._category_key)
        for cog_or_category, commands in grouped_commands:
            sorted_commands = sorted(commands, key=lambda c: c.name)

            if len(sorted_commands) == 0:
                continue

            command_details_list = self.get_command_details(
                sorted_commands,
                return_as_list=True
            )

            # Split cogs or categories which have too many commands to fit in one page
            for idx in range(0, len(sorted_commands), COMMANDS_PER_PAGE):
                truncated_lines = command_details_list[idx:idx + COMMANDS_PER_PAGE]
                joined_lines = ''.join(truncated_lines)

                # The length of commands is for the paginator
                cog_or_category_pages.append(
                    (f'**{cog_or_category}**{joined_lines}', len(truncated_lines))
                )

        pages = list()
        counter = 0
        page = ''

        for page_details, length in cog_or_category_pages:
            counter += length

            if counter > COMMANDS_PER_PAGE:
                # Force new page to group categories/cogs
                counter = length
                pages.append(page)
                page = f'{page_details}\n\n'
            else:
                page += f'{page_details}\n\n'

        if page:
            # Add any remaining command help
            pages.append(page)

        help_embed = PaginatedEmbed(pages=pages)
        help_embed.set_author(name='Commands Help')
        await help_embed.paginate(self.context)


class Help(Cog):
    """Custom paginated embed for bot help."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

        self.old_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self) -> None:
        """Reset the help command when the cog is unloaded."""
        self.bot.help_command = self.old_help_command
