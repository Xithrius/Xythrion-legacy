"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


def kelvin_to_fahrenheit(k: float, r: int = 2) -> float:
    """Converting from Kelvin to Fahrenheit.

    Args:
        k (float): The amount of Kelvin to convert from.
        r (int): Decimal place to round to.

    Returns:
        A floating point number in Fahrenheit.

    Examples:
        >>> print(kelvin_to_fahrenheit(200))
        -99.67

        >>> print(kelvin_to_fahrenheit(200))
        -100.0

    """
    return round(((k - 273.15) * (9 / 5)) + 32, r)


def kelvin_to_celcius(k: float, r: int = 2) -> float:
    """Converting from Kelvin to Celcius.

    Args:
        k (float): The amount of Kelvin to convert from.
        r (int): Decimal place to round to.

    Returns:
        A floating point number in Fahrenheit.

    Examples:
        >>> print(kelvin_to_celcius(200))
        -73.15

        >>> print(kelvin_to_celcius(200))
        -73.0

    """
    return round(k - 273.15, r)
