from typing import Union


def markdown_link(s: str, link: str) -> str:
    """Gets rid of the thinking while creating a link for markdown."""
    return f"[`{s}`]({link})"


def codeblock(code: Union[list[str], str], language: str = "py") -> str:
    """Turns a string or list of strings into a codeblock."""
    pass


def and_join(items: Union[list, tuple], sep: str = ", ") -> str:
    """Joins a list by a separator with an 'and' at the very end for readability."""
    return f"{sep.join(str(x) for x in items[:-1])}{sep}and {items[-1]}"
