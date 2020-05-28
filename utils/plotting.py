"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""

import sys
import numpy as np
import traceback
import typing as t


try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
except Exception as e:
    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def create_graph(x: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                 y: t.Union[np.ndarray, t.Iterable[t.Union[int, float]]],
                 domain: None,
                 range: None) -> str:
    pass
