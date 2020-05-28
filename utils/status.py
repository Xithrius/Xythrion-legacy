"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime

d = datetime.now().replace(microsecond=0)
stamps = '%Y %b %m %a %I %p'.split()
x = [d.strftime(y) if i != len(stamps) - 1 else d.strftime(y).lower() for i, y in enumerate(stamps)]
print(f'{d} :: {x}')
