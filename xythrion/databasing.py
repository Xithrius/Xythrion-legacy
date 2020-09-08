import asyncpg


async def setup_database(pool: asyncpg.pool.Pool) -> None:
    """Setting up all the tables for the Postgres database."""
    async with pool.acquire() as conn:
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
