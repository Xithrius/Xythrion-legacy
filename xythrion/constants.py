from os import environ
from typing import NamedTuple

__all__ = ('Config', 'WeatherAPIs')


class Config(NamedTuple):
    TOKEN = environ.get('BOT_TOKEN')


class WeatherAPIs(NamedTuple):
    EARTH = environ.get('OPENWEATHERMAP_TOKEN')
    MARS = environ.get('NASA_TOKEN')
