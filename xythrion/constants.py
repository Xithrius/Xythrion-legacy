from os import environ
from typing import NamedTuple

__all__ = (
    'Config', 'Postgresql', 'TwitterOAuth', 'WeatherAPIs',
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


class TwitterOAuth(NamedTuple):
    CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET')
    ACCESS_TOKEN_KEY = environ.get('TWITTER_ACCESS_TOKEN_KEY')
    ACCESS_TOKEN_SECRET = environ.get('TWITTER_ACCESS_TOKEN_SECRET')


class WeatherAPIs(NamedTuple):
    EARTH = environ.get('OPENWEATHERMAP_TOKEN')
    MARS = environ.get('NASA_TOKEN')
