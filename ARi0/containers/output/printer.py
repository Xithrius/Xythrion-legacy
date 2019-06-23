'''
>> SoftBot.py
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
'''


# //////////////////////////////////////////////////////////////////////////// #
# Libraries                                                                    #
# //////////////////////////////////////////////////////////////////////////// #
# Built-in modules, third-party modules, custom modules                        #
# //////////////////////////////////////////////////////////////////////////// #


import datetime


"""

Functions for printing to locations with customized uniting

"""


def printc(string: str):
    """
    Customized printing to the console with timestamps
    """
    now = datetime.datetime.now()
    print(f"~> [{now}] {string}")


def duplicate(string: str):
    """
    Prints to console and wherever else
    """
    printc(string)
    return (string[string.index(':') + 2]).upper() + (string[string.index(':') + 3]).lower()


def sectional_print(loaded_cogs):
    """
    Prints cogs out in sections
    """
    all_cogs, sectioned_cogs = [], []
    l_cogs = [x.split('.')[-2:] for x in loaded_cogs]
    for i in range(len(l_cogs) - 1):
        x = [j for j, v in enumerate([x[0] for x in l_cogs]) if v == l_cogs[i][0]]
        if x not in sectioned_cogs:
            sectioned_cogs.append(x)
    for i in range(len(sectioned_cogs)):
        within_cogs = [l_cogs[sectioned_cogs[i][0]][0], [l_cogs[j][1] for j in sectioned_cogs[i]]]
        all_cogs.append(within_cogs)
    for i in all_cogs:
        print(f'\t{i[0]}: {", ".join(str(y) for y in i[1])}')
