"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import datetime
import re


def html_parser(self, soup, search):
    """Uses BeautifulSoup to parse html

    Args:
        soup (bs4.BeautifulSoup): html to be parsed

    Returns:
        A Dictionary of items

    Raises:
        Nothing, unless something cannot be parsed.

    """
    pass


def interval_parser(self, interval: str) -> datetime.datetime:
    """Retrieves a datetime from a string containing certien dates
    Source: https://github.com/Priultimus/flux-discordbot/blob/master/ui/general.py#L18-L28

    Args:
        interval (str): unparsed string of human date

    Returns:
        t (datetime.datetime): final date until time is complete.

    Raises:
        ValueError: parsing cannot be completed.

    """
    t = re.match(r"(?:(?P<weeks>\d+)w)?(?:\s+)?(?:(?P<days>\d+)d)?(?:\s+)?(?:(?P<hours>\d+)h)?(?:\s+)?(?:(?P<minutes>\d+)m)?(?:\s+)?(?:(?P<seconds>\d+)s)?", interval)
    t = t.groupdict()
    for k, v in t.items():
        if t[k] is None:
            t[k] = 0
    for k, v in t.items():
        t[k] = int(v)
    t = datetime.timedelta(weeks=t.get("weeks"), days=t.get("days"), hours=t.get(
        "hours"), minutes=t.get("minutes"), seconds=t.get("seconds"))
    t = datetime.datetime.now() - t
    return t
