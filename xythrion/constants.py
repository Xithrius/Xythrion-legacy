from os import environ
from typing import NamedTuple

__all__ = ("Config", "Postgresql", "WeatherAPIs")


class Config(NamedTuple):
    TOKEN = environ.get("BOT_TOKEN")
    GITHUB_URL = environ.get("GITHUB_URL", "https://github.com/Xithrius/Xythrion")


class Postgresql(NamedTuple):
    USER = environ.get("POSTGRES_USER", "postgres")
    PASSWORD = environ.get("POSTGRES_PASSWORD")
    DATABASE = environ.get("POSTGRES_DB", "postgres")
    HOST = environ.get("POSTGRES_HOST", "localhost")

    asyncpg_config = {
        "user": USER,
        "password": PASSWORD,
        "database": DATABASE,
        "host": HOST,
    }


class WeatherAPIs(NamedTuple):
    EARTH = environ.get("OPENWEATHERMAP_TOKEN")
    MARS = environ.get("NASA_TOKEN")
