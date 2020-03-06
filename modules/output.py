"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import sys
import os
import datetime


def path(*filepath) -> str:
    """Returns absolute path from main caller file to another location.
    
    Args:
        filepath (iritable): Arguments to add to the current filepath.

    Returns:
        String of filepath with OS based seperator.

    """
    lst = [
        os.path.abspath(os.path.dirname(sys.argv[0])),
        (os.sep).join(str(y) for y in filepath)
    ]
    return (os.sep).join(str(s) for s in lst)


def get_extensions() -> list:
    """Gets all the extensions within a folder for the bot to load.
    
    Returns:
        a list of cogs starting with cogs.<folder if any>.<filename without .py>.

    """
    c = []
    
    for folder in os.listdir(path('cogs')):
        c.extend([f'cogs.{folder}.{i[:-3]}' for i in os.listdir(path('cogs', folder)) if i[-3:] == '.py'])

    return c


def gen_filename() -> str:
    """Generates a filename.
    
    Returns:
        A string with the current date for filename usage.

    """
    return str(datetime.datetime.timestamp(datetime.datetime.now())).replace('.', '')


def shorten(s: str, char_limit: int = 50) -> str:
    """Cuts down a string to a specific length and adds '...'

    Args:
        s (str): The input string
        _len (int): The desired limit for length

    Returns:
        A string cut down to a specific length.

    """
    new_str = []
    for word in s.strip().split():
        if len(' '.join(str(y) for y in new_str)) < char_limit:
            new_str.append(word)
        else:
            break

    new_str = ' '.join(str(y) for y in new_str).strip()
    return new_str + '...' if len(new_str) >= char_limit else new_str


def create_title(self):
    """Creates a fancy title"""
    # Colors
    r, d, b, e = '\033[91m', '\033[93m', '\033[1m', '\033[0m'
    
    with open(path('fonts', 'title.txt'), 'r') as f:
        titles = [y[:-1] if '\n' in y else y for y in f.readlines()]

        # Formatting date
        n = datetime.datetime.now()
        t = ':'.join(y for y in n.strftime('%I %M %S').split())
        n = f"{n.strftime('%b %d %Y, %A')} {t}{n.strftime('%p').lower()}"        
        n = f'~> {b}[{e} {d}{n}{e} {b}]{e} >'
        
        print()
        for i, title in enumerate(titles):
            # title = f'{b}{r}{title}{e}{e}'
            if i != 1:
                print(title.rjust(len(n) + 2, ' '))
            else:
                print(n + title.rjust(2, ' '))
        print()
