from xythrion.utils.formatting import and_join, codeblock, markdown_link


def test_markdown_link() -> None:
    link = "https://www.google.com"

    assert markdown_link("google", link) == f"[google]({link})"
    assert markdown_link("google", link, "`") == f"[`google`]({link})"
    assert markdown_link(link, "google") == f"[{link}](google)"


def test_and_join() -> None:
    lst = [1, 2, 3, 4]

    assert and_join(lst) == "1, 2, 3, and 4"
    assert and_join(lst, sep=" ") == "1 2 3 and 4"
    assert and_join(lst, sep="") == "123and 4"


def test_codeblock() -> None:
    code = "print(1 + 2)"
    language = "py"

    assert codeblock(code) == "```python\nprint(1 + 2)\n```"
    assert codeblock(code, language=language) == "```py\nprint(1 + 2)\n```"
