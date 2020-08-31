from os import environ
from typing import NamedTuple

__all__ = (
    'Config', 'Postgresql'
)


class Config(NamedTuple):
    TOKEN = environ.get('BOT_TOKEN')
    BOT_ICON_LINK = environ.get(
        'BOT_ICON_LINK', 'https://raw.githubusercontent.com/Xithrius/Xythrion/master/images/icon.png')
    BOT_DESCRIPTION = environ.get('BOT_DESCRIPTION', 'Graphing manipulated data through discord.py')


class Postgresql(NamedTuple):
    USER = environ.get('POSTGRES_USER')
    PASSWORD = environ.get('POSTGRES_PASSWORD')
    DATABASE = environ.get('POSTGRES_DB')
    HOST = environ.get('POSTGRES_HOST')

    asyncpg_config = {'user': USER, 'password': PASSWORD, 'database': DATABASE, 'host': HOST}
    asyncpg_config_url = f'postgres://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}'
    asyncpg_default_docker_config = {'user': 'postgres', 'database': 'postgres', 'host': 'localhost'}
