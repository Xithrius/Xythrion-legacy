from __future__ import annotations

import asyncio
import collections
import typing as t
from collections.abc import Sequence
from contextlib import suppress

import discord
from discord.ext.commands import Context

FIRST_EMOJI = '⏪'
LEFT_EMOJI = '◀️'
RIGHT_EMOJI = '▶️'
LAST_EMOJI = '⏩'
DELETE_EMOJI = '❌'

PAGINATION_EMOJIS = (FIRST_EMOJI, LEFT_EMOJI, RIGHT_EMOJI, LAST_EMOJI, DELETE_EMOJI)


# Yoinked from: https://github.com/Snek-Network/snek/blob/master/snek/utils/paginator.py


class EmptyPaginatorLines(Exception):
    """Exception for empty paginator lines."""


class LinePaginator(Sequence):
    """Paginator through text."""

    def __init__(self, lines: t.Iterable[str], max_chars: int = 2000, max_lines: t.Optional[int] = None,
                 truncation_msg: str = '...', page_header: str = '', page_prefix: str = '',
                 page_suffix: str = ''
                 ) -> None:
        if not lines:
            raise EmptyPaginatorLines('Cannot paginator empty lines.')

        min_chars = len(truncation_msg) + len(page_header) + len(page_header) + len(page_prefix) + len(
            page_suffix) + 100

        if max_chars < min_chars:
            raise ValueError(
                f'A minimum of {min_chars} characters is needed for pagination. '
                'Please raise the `max_chars` limit.'
            )

        self.lines = collections.deque(lines)
        self.max_chars = max_chars
        self.max_lines = max_lines
        self.truncation_msg = truncation_msg
        self.page_header = page_header
        self.page_prefix = page_prefix
        self.page_suffix = page_suffix

        if self.page_header:
            self.max_chars -= len(self.page_header) + 1

        if self.page_prefix:
            self.max_chars -= len(self.page_prefix) + 1

        if self.page_suffix:
            self.max_chars -= len(self.page_suffix) + 1

        self.pages = list()
        self.current_page = None

        self._remaining_chars = None
        self._index = 0

        # Create the first page
        self.start_page()
        self.create_pages()

    def __len__(self) -> int:
        """Returns the number of pages in the paginator."""
        return len(self.pages)

    def __getitem__(self, page_number: int) -> str:
        """Get a page by its page number."""
        return self.pages[page_number]

    def truncate_line(self, line: str) -> str:
        """
        Truncate a long line and add the remainder back on the line queue.

        If a suitable breakpoint cannot be found (a space), it will break
        on characters instead.
        """
        # Determine a good lower bound to truncate within using a space
        lower_bound = self.max_chars // 8
        upper_bound = self._remaining_chars - len(self.truncation_msg) - 2

        # Find the space to break on
        breakpoint_ = line.rfind(' ', lower_bound, upper_bound)

        if breakpoint_ == -1:
            # Cannot find a space
            # Truncate on characters instead
            breakpoint_ = self.max_chars - len(self.truncation_msg)

        # Add the remainder to the next page
        line, next_line = line[:breakpoint_] + self.truncation_msg, line[breakpoint_:]
        self.lines.appendleft(next_line)

        return line

    def create_pages(self) -> None:
        """Create pages using the constraints given."""
        while self.lines:
            # Get a line from the beginning of the queue
            line = self.lines.popleft()

            # This line is longer than one page
            if len(line) > self.max_chars:
                # Check if current page has enough space to add
                # a piece of the long line.
                if self._remaining_chars <= self.max_chars // 4:
                    self.start_page()

                # Truncate line and add the remainder back on the line queue
                line = self.truncate_line(line)

            # Close the current page if the line does not fit
            if self._remaining_chars < len(line) + 2:
                self.start_page()

            if self.max_lines and len(self.current_page) >= self.max_lines:
                self.start_page()

            line = line.rstrip()
            if not line:
                continue

            # Append this line and update remaining characters
            self.current_page.append(line)
            self._remaining_chars -= len(line) + 2

        # Close the final page once finished
        self.start_page()

    def start_page(self) -> None:
        """Close a page once it's been created and start a new one."""
        if self.current_page:
            self.current_page.append(self.page_suffix)
            self.pages.append('\n'.join(self.current_page))

        self.current_page = [self.page_prefix] if self.page_prefix else []

        if self.page_header:
            self.current_page.append(self.page_header)

        self._remaining_chars = self.max_chars


class PaginatedEmbed(discord.Embed):
    """
    Paginates the description of an embed.

    There is an alternative constructor, `from_lines`, which accepts
    an iterable of lines and creates a `LinePaginator`.
    """

    def __init__(self, pages: t.Sequence, timeout: int = 120, **kwargs) -> None:
        super().__init__(**kwargs)

        if not pages:
            pages = ["[There's nothing to show here]"]

        self.pages = pages
        self.current_page = 0
        self.last_page = len(pages) - 1

        self.timeout = timeout

        self._footer_text = discord.Embed.Empty
        self._message = None
        self._context = None
        self.owner = None

        self.new_page_number = {
            FIRST_EMOJI: lambda _: 0,
            LEFT_EMOJI: lambda current_page: max(current_page - 1, 0),
            RIGHT_EMOJI: lambda current_page: min(current_page + 1, self.last_page),
            LAST_EMOJI: lambda _: self.last_page
        }

    @classmethod
    def from_lines(cls, lines: t.Iterable[str], **kwargs) -> PaginatedEmbed:
        """Creates a `PaginatedEmbed` with a `LinePaginator`."""
        max_chars = kwargs.pop('max_chars', 2000)
        max_lines = kwargs.pop('max_lines', None)
        truncation_msg = kwargs.pop('truncation_msg', '...')
        page_header = kwargs.pop('page_header', '')
        page_prefix = kwargs.pop('page_prefix', '')
        page_suffix = kwargs.pop('page_suffix', '')

        paginator = LinePaginator(
            lines=lines,
            max_chars=max_chars,
            max_lines=max_lines,
            truncation_msg=truncation_msg,
            page_header=page_header,
            page_prefix=page_prefix,
            page_suffix=page_suffix
        )
        return cls(pages=paginator, **kwargs)

    async def paginate(
            self,
            ctx: Context,
            message_content: t.Optional[str] = None,
            owner: t.Optional[discord.Member] = None,
            **message_kwargs
    ) -> discord.Message:
        """
        Start pagination be sending the paginated embed to `ctx.channel'.

        Add content to the message containing the embed by using the
        `message_content` parameter. `message_kwargs` will also be
        passed to `ctx.send`.

        Restrict pagination to a specific user by providing an `owner`.
        """
        if 'embed' in message_kwargs:
            message_kwargs.pop('embed')

        self.description = self.pages[self.current_page]

        if len(self.pages) == 1:
            # No need to paginate with only one page
            return await ctx.send(message_content, embed=self, **message_kwargs)

        self.owner = owner

        self.set_footer()
        self._message = await ctx.send(message_content, embed=self, **message_kwargs)
        self._context = ctx

        await self._start_interface()
        return self._message

    def check(self, reaction: discord.Reaction, user: discord.User) -> bool:
        """Check if `reaction` is a valid pagination attempt for the embed."""
        # Reaction on different message
        if reaction.message.id != self._message.id:
            return False

        # Bot should not react to its own reactions
        if user.id == self._context.bot.user.id:
            return False

        # User is not the owner of the embed
        if self.owner and self.owner.id != user.id:
            return False

        # An unsupported emoji used
        if str(reaction.emoji) not in PAGINATION_EMOJIS:
            return False

        # All tests have passed
        return True

    async def _start_interface(self) -> None:
        """Start the pagination interface for the user."""
        for emoji in PAGINATION_EMOJIS:
            await self._message.add_reaction(emoji)

        while True:
            try:
                reaction, user = await self._context.bot.wait_for(
                    'reaction_add',
                    timeout=self.timeout,
                    check=self.check
                )

            except asyncio.TimeoutError:
                await self._close_interface()
                return

            if reaction.emoji == DELETE_EMOJI:
                await self._close_interface()
                return

            new_page = self.new_page_number[reaction.emoji](self.current_page)
            if new_page != self.current_page:
                self.current_page = new_page

                if not await self._change_page():
                    return

            with suppress(discord.NotFound):
                await self._message.remove_reaction(reaction.emoji, user)

    async def _close_interface(self) -> None:
        """Close the pagination interface."""
        with suppress(discord.NotFound):
            await self._message.clear_reactions()

    async def _change_page(self) -> bool:
        """Change the currently visible page in the embed."""
        self.set_footer()
        self.description = self.pages[self.current_page]

        try:
            await self._message.edit(content=self._message.content, embed=self)
        except discord.NotFound:
            return False

        return True

    def set_footer(self, **kwargs) -> None:
        """Set the footer text of the embed, including `text` and the page number."""
        if len(self.pages) == 1:
            # No need to set footer ourselves if there's one page
            super().set_footer(**kwargs)
            return

        if 'text' in kwargs:
            self._footer_text = kwargs.pop('text')

        text = f'Page {self.current_page + 1} / {len(self.pages)}'
        if self._footer_text:
            text = f'{self._footer_text} ({text})'

        super().set_footer(text=text, **kwargs)
