"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from typing import NamedTuple
import os


__all__ = (
    'Postgresql',
    'Config',
)


class Postgresql(NamedTuple):
    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    DATABASE = os.environ.get('POSTGRES_DB')
    HOST = os.environ.get('POSTGRES_HOST')

    asyncpg_config = {'user': USER, 'password': PASSWORD, 'database': DATABASE, 'host': HOST}
    asyncpg_config_url = f'postgres://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}'
    asyncpg_default_docker_config = {'user': 'postgres', 'database': 'postgres', 'host': 'localhost'}


class Config(NamedTuple):
    TOKEN = os.environ.get('BOT_TOKEN')
