"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import json
from asyncio import AbstractEventLoop
from typing import Optional, Union

from aiohttp import ClientSession


def gen_block(content: Union[str, list, dict], *, lang: str = 'py', lines: bool = False) -> str:
    """Generates a Discord markdown block.

    Args:
        content (:obj:`typing.Union[str, list, dict]`): What will be converted into a block.
        language (str, optional): The markdown language.
        lines (bool, optional): The option to insert line numbers at the start of every line.

    Returns:
        A string containing a programming language block for Discord.

    Examples:
        >>> print(gen_block(['item', 'another item']))
        ```py
        item
        another item
        ```

        >>> print(gen_block('item', 'css'))
        ```css
        item
        ```

        >>> print(gen_block({
            'key1': 'value1',
            'another key': 'wow another value'
        }, lines=True))
        ```py
        000 | {
        001 |     'key1': 'value1',
        002 |     'another key': 'wow another value'
        003 | }
        ```
    """
    if isinstance(content, dict):
        content = json.dumps(content, indent=3, sort_keys=True).split('\n')

    if isinstance(content, list):
        content = '\n'.join(f'{str(i).zfill(3)} | {str(y)}' if lines else (str(y)) for i, y in enumerate(content))

    return f'```{lang}\n{content}\n```'


async def http_get(url: str, *, session: ClientSession = None, loop: Optional[AbstractEventLoop] = None, block: bool = False) -> Union[dict, str]:
    """Gets information from a http request.

    Args:
        url (str): The url that the service is located at.
        session (aiohttp.ClientSession, optional): The session that will be used for the request.
        loop (:obj:`Optional[asyncio.AbstractEventLoop]`, optional): The loop that will be used for the session.
        block (bool, optional): if you want the response to be inserted into a Discord markdown block.

    Returns:
        A Discord markdown block returned by gen_block or a dictionary from the service response.

    Raises:
        Assertion error with status code if not 200

    Examples:
        >>> print(await http_get('https://httpbin.org/get'))
        {
        "args": {},
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Host": "httpbin.org",
            "User-Agent": "Python/3.8 aiohttp/3.6.2",
            "X-Amzn-Trace-Id": "██████████████████████████████████ (Just in case)"
        },
        "origin": "██████████████████████ (it's your ip)",
        "url": "https://httpbin.org/get"
        }

        >>> print(await http_get('https://httpbin.org/get', block=True))
        ```py
        000 | {
        001 | "args": {},
        002 | "headers": {
        003 |     "Accept": "*/*",
        004 |     "Accept-Encoding": "gzip, deflate",
        005 |     "Host": "httpbin.org",
        006 |     "User-Agent": "Python/3.8 aiohttp/3.6.2",
        007 |     "X-Amzn-Trace-Id": "██████████████████████████████████ (Just in case)"
        008 | },
        009 | "origin": "██████████████████████ (it's your ip)",
        010 | "url": "https://httpbin.org/get"
        011 | }
        ```

    """
    session = ClientSession(loop=loop) if not session else session
    async with session.get(url) as r:
        assert r.status == 200, r.status
        content_type = r.content_type.split('/')[1]

        try:
            info = await r.json()
        except TypeError:
            info = await r.html()

        if block:
            return gen_block(dict(info), lang='py' if content_type == 'json' else content_type, lines=True)

        return info
