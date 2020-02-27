"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


def kelvin_to_fahrenheit(k, _round=2) -> float:
    return round(((k - 273.15) * (9 / 5)) + 32, _round)


def kelvin_to_celcius(k, _round=2) -> float:
    return round(k - 273.15, _round)
