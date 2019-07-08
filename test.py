import os

from handlers.modules.output import path, printc


def sectional_print(loaded_cogs):
    """ Prints cogs out in sections """
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


def sectional_table(extension_dict):
    longest_extension = [k, v for k, v in extension_dict.items()]
