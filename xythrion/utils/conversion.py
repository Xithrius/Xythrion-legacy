def k2f(k: float, r: int = 2) -> float:
    """Kelvin to Fahrenheit"""
    return round(((k - 273.15) * (9 / 5)) + 32, r)


def k2c(k: float, r: int = 2) -> float:
    """Kelvin to Celsius"""
    return round(k - 273.15, r)


def c2k(c: float, r: int = 2) -> float:
    """Celsius to Kelvin"""
    return round(c + 273.15, r)


def c2f(c: float, r: int = 2) -> float:
    """Celsius to Fahrenheit"""
    return round((c * 1.8) + 32, r)
