'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


def index_days(lst: list, day: int):
    days = ['m', 't', 'w', 'th', 'f']
    if days[day] in lst:
        return True
