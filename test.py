import os
from containers.essentials.pathing import path


essential_cogs = []
for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
    essential_cogs.extend(filenames)
    break

custom_cogs = []
for (dirpath, dirnames, filenames) in os.walk(path('cogs', 'rack')):
    custom_cogs.extend(filenames)
    break

cogs = []
for file in essential_cogs:
    if file[-3:] == '.py':
        cogs.append(f'cogs.{file[:-3]}')

for file in custom_cogs:
    if file[-3:] == '.py':
        cogs.append(f'cogs.rack.{file[:-3]}')

for i in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r')]:
    for j in cogs:
        if j in [f'cogs.{i}', f'cogs.rack.{i}']:
            cogs.pop(cogs.index(j))
