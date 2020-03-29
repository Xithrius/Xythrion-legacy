"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import json
import os
import sys
import typing as t
from datetime import datetime, timedelta
from http.client import responses
import asyncio
import functools
import discord

import numpy as np
from aiohttp import ClientSession


def path(*filepath) -> str:
    """Returns absolute path from main caller file to another location.

    Args:
        filepath (iritable): Arguments to add to the current filepath.

    Returns:
        String of filepath with OS based seperator.

    Examples:
        >>> print(path('tmp', 'image.png'))
        C:\\Users\\Xithr\\Documents\\Repositories\\Xythrion\\tmp\\image.png

    """
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


def gen_block(content: t.Union[str, list, dict], *,
              lang: str = 'py', lines: bool = False, separator: str = '|') -> str:
    """Generates a Discord markdown block.

    Args:
        content (:obj:`typing.Union[str, list, dict]`): What will be converted into a block.
        language (str, optional): The markdown language.
        lines (bool, optional): The option to insert line numbers at the start of every line.
        separator (str, optional): The separator between the line number and information

    Returns:
        A string containing a programming language block for Discord.

    Examples:
        >>> print(gen_block(['item', 'another item']))
        ```py
        item
        another item
        ```

        >>> print(gen_block('item', lang='css'))
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

    content = '\n'.join(
        f'{str(i).zfill(3)} {separator} {str(y)}' if lines else (str(y)) for i, y in enumerate(content)
    )

    return f'```{lang}\n{content}\n```'


async def http_get(url: str, *, session: ClientSession = None, block: bool = False) -> t.Union[dict, str]:
    """Gets information from a http request.

    Args:
        url (str): The url that the service is located at.
        session (aiohttp.ClientSession, optional): The session that will be used for the request.
        loop (:obj:`asyncio.AbstractEventLoop`, optional): The loop that will be used for the session.
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
    session = ClientSession() if not session else session
    async with session.get(url) as r:
        assert r.status == 200, f'Status code: {r.status}, {responses[r.status]}.'
        content_type = r.content_type.split('/')[1]

        try:
            info = await r.json()
        except TypeError:
            info = await r.html()

        if block:
            return gen_block(dict(info), lang='py' if content_type == 'json' else content_type, lines=True)

        return info


def gen_filename() -> str:
    """Generates a filename.

    Returns:
        A string with the current date for filename usage.

    Examples:
        >>> print(gen_filename())
        1584774125328021

        >>> print(f'{gen_filename()}.png')
        1584774141733494.png

    """
    return str(datetime.timestamp(datetime.now())).replace('.', '')


def get_extensions() -> list:
    """Gets all the extensions within a folder for the bot to load.

    Returns:
        a list of cogs starting with cogs.<folder if any>.<filename without .py>.

    Examples:
        >>> print(get_extensions())
        ['cogs.math.calculator', 'cogs.math.graphing', 'cogs.meta.custom']

    """
    c = []

    for folder in os.listdir(path('cogs')):
        c.extend([f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py'])

    return c


def shorten(s: str, char_limit: int = 50) -> str:
    """Cuts down a string to a specific length and adds '...'

    Args:
        s (str): The input string
        char_limit (int): The desired limit for length

    Returns:
        A string cut down to a specific length.

    Examples:
        >>> print(shorten("A large string that's very very very long and pretty much never ending until now"))
        A large string that's very very very long and pretty...

        >>> print(shorten("A large string that's very very very long."))
        A large string that's very very very long.

    """
    new_str = []
    for word in s.strip().split():
        if len(' '.join(str(y) for y in new_str)) < char_limit:
            new_str.append(word)
        else:
            break

    new_str = ' '.join(str(y) for y in new_str).strip()
    return new_str + '...' if len(new_str) >= char_limit else new_str


def describe_date(d: timedelta) -> str:
    """Gives hours, minutes, and seconds of a date.

    Args:
        d (:obj:`datetime.timedelta`): The amount of time between two dates.

    Returns:
        A string with an explained timedelta.

    Examples:
        >>> d = datetime(2020, 3, 16, 11, 59)
        >>> print(describe_date(datetime.now() - d))
        10 days, 1 hours, 49 minutes, 19 seconds

    """
    ts = ['hours', 'minutes', 'seconds']
    days, d = str(d).split(', ')
    d = [f'{int(float(t))} {ts[i]}' for i, t in enumerate(d.split(':')) if float(t)]
    return ', '.join(str(y) for y in [days] + d)


def gen_table(lst: t.List[list], *, columns: list = None, rows: list = None,
              s: str = ' | ', block: bool = False) -> t.Union[str, list]:
    """Generating a table for data.

    Args:
        internal_data (:obj:`typing.List[list]`): A 2D list containing table information.
        columns (list, optional): The column titles.
        rows (list, optional): The row titles.
        s (str, optional): The seperator between columns.
        block (bool, optional): Converting this table into a Discord code block with function gen_block.

    Returns:
        A table with column and/or row titles of data, adjusted right to the longest column string.

    Examples:
        >>> print('\n'.join(str(y) for y in gen_table(
                [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
            )))
        1 1 1
        2 2 2
        3 3 3
        4 4 4

        >>> print('\n'.join(str(y) for y in gen_table(
                [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]],
                columns=['column', 'columnn 2', 'column 3']
            )))
        column | columnn 2 | column 3
        ------ | --------- | --------
             1 |         1 |        1
             2 |         2 |        2
             3 |         3 |        3
             4 |         4 |        4

        >>> print('\n'.join(str(y) for y in gen_table(
                [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]],
                rows=['column', 'columnn 2', 'column 3'],
                columns=['column', 'columnn 2', 'column 3']
            )))
                  | column | columnn 2 | column 3
        --------- | ------ | --------- | --------
           column |      1 |         1 |        1
        columnn 2 |      2 |         2 |        2
         column 3 |      3 |         3 |        3

    """
    lst = np.array([columns] + lst if columns else lst)
    # print(lst, '\n', lst.shape)
    m = [max(map(len, [str(y) for y in lst[:, i]])) for i in range(lst.shape[1])]

    if columns:
        lst = [[str(y).rjust(m[i]) for i, y in enumerate(x)] for x in lst]
        lst = np.array(lst)

        sep = ['-' * m[i] for i in range(lst.shape[1])]

        lst = list(lst)
        lst.insert(1, sep)
        if not rows:
            lst = [s.join(str(y) for y in x) for x in lst]

    if rows:
        m_rows = max(map(len, [str(y) for y in rows]))
        rows = [str(x).rjust(m_rows) for x in rows]
        if columns:
            rows = [' ' * m_rows, '-' * m_rows] + rows
            tmp = np.array(lst)
            m = [max(map(len, [str(y) for y in tmp[:, i]])) for i in range(tmp.shape[1])]

        lst = [[f'{y}{" |" if i != len(x) - 1 else ""}'.rjust(m[i]) for i, y in enumerate(x)] for x in lst]
        lst = [y + s + ' '.join(x) for x, y in zip(lst, rows)]

    if not rows and not columns:
        lst = [[str(y).rjust(m[i]) for i, y in enumerate(x)] for x in lst]
        lst = [f' '.join(x) for x in lst]

    return lst


async def lock_executor(func: t.Union[functools.partial, callable],
                        args: list = None, *,
                        loop: asyncio.AbstractEventLoop = None):
    """Uses an asyncio lock to run an synchronous function asynchronously.

    Args:
        func (:obj:`t.Union[functools.partial, callable]`): Either a partial function or a callable.
        args (list, optional): Arguments for the function if not a callable.
        loop (:obj:`asyncio.AbstractEventLoop`, optional): The loop to be used for the executor.

    Returns:
        Whatever the function returns.

    Examples:
        >>> import requests
        >>> url = 'https://httpbin.org/get
        >>> print(
                await lock_executor(requests.get(url).json())
            )
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

    """
    lock = asyncio.Lock()

    loop = asyncio.get_running_loop() if not loop else loop

    async with lock:
        if isinstance(func, functools.partial) or args is None:
            return await loop.run_in_executor(None, func)
        else:
            return await loop.run_in_executor(None, func, *args)


def embed_attachment(p: str) -> tuple:
    """Creating an embed and adding a local image to it.

    Args:
        p (str): The absolute path for the file of the image.

    Returns:
        a file and embed object.

    Examples:
        >>> embed_attachment(path('tmp', 'image.png'))

    """
    f = p.split(os.sep)[-1]
    file = discord.File(p, filename=f)
    embed = discord.Embed()
    embed.set_image(url=f'attachment://{f}')
    return file, embed
