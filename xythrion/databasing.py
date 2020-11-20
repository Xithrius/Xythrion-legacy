import asyncio
import logging
from typing import Optional

import asyncpg
from discord.ext.commands import Context

from .constants import Postgresql

log = logging.getLogger(__name__)


class DatabaseSetup:
    """Setting up the database before the bot initializes completely."""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop

        if not loop:
            self.loop = asyncio.get_event_loop()

        self.pool = self.loop.run_until_complete(self.create_asyncpg_pool())
        self.tables = self.loop.run_until_complete(self.check_tables())

    @staticmethod
    async def create_asyncpg_pool() -> Optional[asyncpg.pool.Pool]:
        """Attempting to connect to the database."""
        try:
            return await asyncpg.create_pool(**Postgresql.asyncpg_config, command_timeout=60)

        except Exception as e:
            log.error(
                "Failed to connect to Postgresql database",
                exc_info=(type(e), e, e.__traceback__),
            )

    async def check_tables(self) -> None:
        """Setting up all the tables for the Postgres database."""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS Links(
                        identification serial PRIMARY KEY,
                        t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        id BIGINT,
                        name TEXT,
                        link TEXT
                    )
                """
            )
            await conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS Dates(
                        identification serial PRIMARY KEY,
                        t TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        id BIGINT,
                        name TEXT
                    )
                """
            )
            await conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS Blocked_Guilds(
                        identification serial PRIMARY KEY,
                        guild_id BIGINT
                    )
                """
            )
            await conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS Blocked_Users(
                        identification serial PRIMARY KEY,
                        user_id BIGINT
                    )
                """
            )


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
            user = await conn.fetch("SELECT * FROM Blocked_Users WHERE user_id = $1", ctx.author.id)

            if not len(user):
                # If the user is not blocked, check if the guild is blocked.
                guild = await conn.fetch("SELECT * FROM Blocked_Guilds WHERE guild_id = $1", ctx.guild.id)

                if not len(guild):
                    return True

        # If none of the checks passed, either the guild or the user is blocked.
        return False
