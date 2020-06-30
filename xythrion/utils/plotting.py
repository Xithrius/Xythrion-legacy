"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import typing as t

import numpy as np

from .shortcuts import tracebacker, get_filename
from pathlib import Path


try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')

except Exception as e:
    tracebacker(e)


def create_plot(x: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                y: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                *,
                domain: t.Optional[t.Union[np.ndarray, t.Iterable[t.Union[int, float]]]] = None,
                range: t.Optional[t.Union[np.ndarray, t.Iterable[t.Union[int, float]]]] = None,
                graph_type: str = 'line'
                ) -> str:
    plt.clf()

    for x, y in zip(x, y):
        plt.bar(x, y)

    f = f'{get_filename()}.png'
    plt.savefig(Path.cwd() / 'tmp' / f)
    return f
