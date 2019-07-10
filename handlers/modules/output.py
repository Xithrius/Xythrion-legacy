"""
>> Xiux
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import __main__
import datetime
import os
import aiohttp


def path(*objects):
    """ Returns path relative to caller file location with additional objects, if any """
    newPath = ((__main__.__file__).split(os.sep))[:-1]
    for i in objects:
        newPath.append(i)
    return (os.sep).join(str(y) for y in newPath)


def printc(string):
    """ Customized printing to the console with timestamps """
    now = datetime.datetime.now()
    print(f"~> [{now}] {string}")


def duplicate(string: str):
    """ Prints to console and wherever else """
    printc(string)
    return (string[string.index(':') + 2]).upper() + (string[string.index(':') + 3]).lower()


def create_table(cogs_dict):
    """ """
    keys, cogs = [], []
    for k, v in cogs_dict.items():
        keys.append(k)
        cogs.append(', '.join(str(y)[:-3] for y in v))
    longest_cog_name = max(map(len, keys))
    longest_cog_line = max(map(len, cogs))
    print()
    for i in range(len(keys)):
        print(f'\t+{"-" * (longest_cog_name + 2)}+{"-" * (longest_cog_line + 2)}+')
        print(f'\t| {keys[i]}{" " * (longest_cog_name - len(keys[i]))} | {cogs[i]}{" " * (longest_cog_line - len(cogs[i]))} |')
    print(f'\t+{"-" * (longest_cog_name + 2)}+{"-" * (longest_cog_line + 2)}+')
    print()


def now():
    """ Returns the time depending on time zone from file """
    return datetime.datetime.now() + datetime.timedelta(hours=7)


def progress_bar(iteration, total, prefix='PROGRESS:', suffix='COMPLETE', decimals=2, length=50, fill='█'):
    """ Progress bar for tracking progress """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


async def aiohttp_requester(ctx, option, url, headers, data=None):
    """ Gets data from a REST API """
    async with aiohttp.ClientSession() as session:
        if option == 'GET':
            async with session.get(url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    await ctx.send(f'Status {response.status}: Requester unavailable')
        elif option == 'POST':
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    await ctx.send(f'Status {response.status}: Requester unavailable')
