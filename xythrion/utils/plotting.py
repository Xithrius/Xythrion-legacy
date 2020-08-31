from pathlib import Path
from typing import Iterable, Union

import numpy as np

from .shortcuts import gen_filename

try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.style.use('dark_background')

except Exception as e:
    print(e)


def create_plot(x: Union[np.ndarray, Iterable[Union[int, float]]],
                y: Union[np.ndarray, Iterable[Union[int, float]]]) -> str:
    """
    Attempting to make a graph from the void.

    Dynamic numpy arange by getting difference in domain and dividing by like 50.
    """
    plt.clf()

    np.arange()

    for x, y in zip(x, y):
        plt.bar(x, y)

    f = f'{gen_filename()}.png'
    plt.savefig(Path.cwd() / 'tmp' / f)
    return f
