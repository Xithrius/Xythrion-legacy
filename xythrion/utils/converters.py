import re


whitespace_pattern = re.compile(r"\s+")


def remove_whitespace(argument: str) -> str:
    """Replaces any whitespace within a string with nothingness."""
    return re.sub(whitespace_pattern, "", argument)
