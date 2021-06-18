from datetime import datetime

from typing import Sequence


def markdown_link(s: str, link: str, t: str = "") -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    return f"[{t}{s}{t}]({link})"


def and_join(items: Sequence, sep: str = ", ") -> str:
    """Joins a list by a separator with an 'and' at the very end for readability."""
    items = items if isinstance(items, list) else list(items)

    return f"{sep.join(str(x) for x in items[:-1])}{sep}and {items[-1]}"


def codeblock(code: str, language: str = "python") -> str:
    """Returns a string in the format of a Discord codeblock."""
    return f"```{language}\n{code}\n```"


def epoch_to_datetime(epoch: int, time_format: str = "%b %m %H:%M") -> str:
    """Gets unix time, and in return gives a formatted string of said time."""
    return datetime.strftime(datetime.fromtimestamp(epoch), time_format)
