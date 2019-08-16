"""
>> Xylene
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import __main__
import datetime
import os
import asyncio


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


def now():
    """ Returns the time depending on time zone from file """
    return datetime.datetime.now()


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


def progress_bar(iteration, total, prefix='PROGRESS:', suffix='COMPLETE', decimals=2, length=50, fill='█'):
    """ Progress bar for tracking progress """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def get_cogs(blocked_cogs):
    """ Gets '.' joined filepaths for one iteration of folders within the 'cogs' folder """
    folders = [folder for folder in os.listdir(path('cogs')) if folder != '__pycache__']
    exts = []
    for folder in folders:
        folder_cogs = [f'cogs.{folder}.{cog[:-3]}' for cog in os.listdir(path('cogs', folder)) if os.path.isfile(path('cogs', folder, cog)) and cog[:-3] not in blocked_cogs]
        exts.extend(folder_cogs)
    return exts


def get_filename(id, end=''):
    return f'{int(datetime.datetime.timestamp((now())))}-{id}{end}'
