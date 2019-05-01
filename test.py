import os
from containers.essentials.pathing import path

cogs = []
for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
    cog = '.'.join(str(y) for y in dirpath[len(path()) + 1:].split('\\'))
    if '__pycache__' not in cog:
        for i in filenames:
            cogs.append(f'{cog}.{i[:-3]}')
print(cogs)

for i in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r')]:
    for j in cogs:
        if list(i) in list(j):
            cogs.pop(cogs.index(j))
print(cogs)


'''
cogs.extend([f'cogs.{file[:-3]}' for file in essential_cogs if file[-3:] == '.py'])
cogs.extend([f'cogs.rack.{file[:-3]}' for file in custom_cogs if file[-3:] == '.py'])

for i in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r')]:
    for j in cogs:
        if j in [f'cogs.{i}', f'cogs.rack.{i}']:
            cogs.pop(cogs.index(j))
'''
