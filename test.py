import os
from containers.essentials.pathing import path


cogs = []
for (dirpath, dirnames, filenames) in os.walk(path('cogs')):
    cog = '.'.join(str(y) for y in dirpath[len(path()):].split('\\'))
    if '__pycache__' not in cog:
        cogs.extend([f'{cog}.{i[:-3]}' for i in filenames if i[:-3] not in [x[:-1] for x in open(path('relay', 'configuration', 'blocked_cogs.txt'), 'r').readlines()]])
print(cogs)