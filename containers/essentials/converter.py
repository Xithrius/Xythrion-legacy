'''

+----[ Relay.py ]-------------------------------+
|                                               |
|  Copyright (c) 2019 Xithrius                  |
|  MIT license, Refer to LICENSE for more info  |
|                                               |
+-----------------------------------------------+

'''


"""

Conversion between two values

"""
def index_days(lst: list, day: int):
    """
    Converting days to numerical values
    """
    days = ['m', 't', 'w', 'th', 'f']
    if days[day] in lst:
        return True
