import asyncio
import functools
import logging
from typing import Any, Callable, Optional, Tuple, Union

import asyncpg
from discord.ext.commands import Context

from .constants import Postgresql

log = logging.getLogger(__name__)


def build_where_string(func: Callable) -> Callable:
    """Creating strings out of iterables so fetch/executions of the Postgresql database are easier."""

    @functools.wraps(func)
    async def wrapper(**kwargs) -> None:
        """Modifying the where and items kwargs, if they exist into strings."""
        where = kwargs.get('where')
        where_str = ' AND '.join(f'{k} = ${i}' for i, k in enumerate(where.keys(), start=1))
        kwargs['where'] = (where_str, list(where.values()))

        if 'items' in kwargs.keys():
            items = kwargs.get('items', None)

            if items != '*' and isinstance(items, tuple) and len(items) > 1:
                kwargs['items'] = f'({", ".join(items)})'

        result = await func(**kwargs)

        return result

    return wrapper


class DatabaseSetup:
    """Setting up the database before the bot initializes completely."""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop

        if not loop:
            self.loop = asyncio.get_event_loop()

        self.pool = self.loop.run_until_complete(self.create_asyncpg_pool())
        self.tables = self.loop.run_until_complete(self.setup_tables())

    @staticmethod
    async def create_asyncpg_pool() -> Optional[asyncpg.pool.Pool]:
        """Attempting to connect to the database."""
        try:
            return await asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60)

        except Exception as e:
            log.critical(f'Failed to connect to Postgresql database: {e}')

    async def setup_tables(self) -> Optional[bool]:
        """Setting up all the tables for the Postgres database."""
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('''
                        CREATE TABLE IF NOT EXISTS Links(
                            identification serial PRIMARY KEY,
                            t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                            id BIGINT,
                            name TEXT,
                            link TEXT
                        )
                    ''')
                await conn.execute('''
                        CREATE TABLE IF NOT EXISTS Dates(
                            identification serial PRIMARY KEY,
                            t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                            id BIGINT,
                            name TEXT
                        )
                    ''')
                await conn.execute('''
                        CREATE TABLE IF NOT EXISTS Blocked_Guilds(
                            identification serial PRIMARY KEY,
                            guild_id BIGINT
                        )
                    ''')
                await conn.execute('''
                        CREATE TABLE IF NOT EXISTS Blocked_Users(
                            identification serial PRIMARY KEY,
                            user_id BIGINT
                        )
                    ''')

            return True

        except Exception as e:
            log.critical(f'Could not complete setup of tables for Postgresql database: {e}')


class Database(DatabaseSetup):
    """Utilities for the database, inheriting from setup."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        """The name of the host of the database."""
        return Postgresql.HOST

    def __bool__(self) -> bool:
        """If the database is not available."""
        return all((self.pool, self.tables))

    async def check_if_blocked(self, ctx: Context) -> bool:
        """Checks if user/guild is blocked."""
        async with self.pool.acquire() as conn:
            # Check if user is blocked.
            user = await conn.fetch('SELECT * FROM Blocked_Users WHERE user_id = $1', ctx.author.id)

            if not len(user):
                # If the user is not blocked, check if the guild is blocked.
                guild = await conn.fetch('SELECT * FROM Blocked_Guilds WHERE guild_id = $1', ctx.guild.id)

                if not len(guild):
                    return True

        # If none of the checks passed, either the guild or the user is blocked.
        return False

    @build_where_string
    async def select(self, *, table: str, items: Union[Tuple[Any], str] = '*', where: Tuple[str, str]
                     ) -> asyncpg.Record:
        """
        Select value(s) from the Postgresql database.

        Example: 'SELECT * FROM table WHERE guild_id = $1 AND something_else = $2'
        """
        async with self.pool.acquire() as conn:
            return conn.fetch(
                f'SELECT {items} FROM {table} {"WHERE " + where[0] if where else ""}', *where[1]
            )

    @build_where_string
    async def insert(self, *, table: str, items: Union[Tuple[Any], str] = '*', where: Tuple[str, str]
                     ) -> asyncpg.Record:
        """
        Insert value(s) from the Postgresql database.

        Example: 'INSERT INTO table(item, item2) VALUES($1, $2)', something, another
        """
        async with self.pool.acquire() as conn:
            return conn.execute(
                f'INSERT INTO {table} VALUES'
            )

    @build_where_string
    async def delete(self, *, table: str, where: str) -> asyncpg.Record:
        """
        Delete value(s) from the Postgresql database.

        Example: 'DELETE FROM table WHERE something = $1 AND another_thing = $2', something, another
        """
        pass
