"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


class Property:
    def __init__(self, type_=None, cond=None):
        self.type_ = type_
        self.cond = cond

    def __set__(self, instance, value):
        self.check(value)
        self.value = value

    def __get__(self, instance):
        return self.value

    def check(self, value):
        if self.type_ is not None and not isinstance(value, self.type_):
            raise ValueError(f'Expected {self.type_}: got {type(value)}')

        if self.cond is not None and not self.cond(value):
            raise ValueError(f'Does not meet {self.cond}')


# In [10]: class Test:
#     ...:     x = Property(int, lambda x: x > 0)
#     ...:     y = Property(float, lambda y: 1 <= y <= 10)
#     ...:
#     ...:     def __init__(self, x, y):
#     ...:         self.x = x
#     ...:         self.y = y

# In [11]: Test(2, 2.5)
# Out[11]: <__main__.Test at 0x7fa563bb8df0>

# In [12]: Test(2.5, 2.5)
# ...
# ValueError: Expected <class 'int'>: got <class 'float'>

# NOTE: You can also do this:

# In [16]: class Test:
#     ...:     def __init__(self, x):
#     ...:         self.x = x
#     ...:     @property
#     ...:     def x(self):
#     ...:         return self._x
#     ...:     @x.setter
#     ...:     def x(self, value):
#     ...:         if not isinstance(value, int):
#     ...:             raise ValueError(f'Expected {int}, got: {value}')
#     ...:         self._x = value

# In [17]: Test(10)
# Out[17]: <__main__.Test at 0x7fa563e282e0>

# In [18]: Test(10.5)
# ...
# ValueError: Expected <class 'int'>, got: 10.5
