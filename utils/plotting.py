"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing as t

import numpy as np

from . import tracebacker


try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')

except Exception as e:
    tracebacker(e)


def create_graph(x: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                 y: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                 domain: None,
                 range: None) -> str:
    pass
