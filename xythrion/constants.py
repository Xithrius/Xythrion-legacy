from os import environ
from typing import NamedTuple

__all__ = ("Config", "WeatherAPIs")


class Config(NamedTuple):
    TOKEN = environ.get("BOT_TOKEN")
    GITHUB_URL = environ.get("GITHUB_URL", "https://github.com/Xithrius/Xythrion")


class WeatherAPIs(NamedTuple):
    EARTH = environ.get("OPENWEATHERMAP_TOKEN")
    MARS = environ.get("NASA_TOKEN")
