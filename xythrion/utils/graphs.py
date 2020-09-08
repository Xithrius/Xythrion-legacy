import logging
import re
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
from sympy import symbols, sympify

from .shortcuts import gen_filename

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.style.use('dark_background')

except Exception as e:
    log.error(f'Error when importing matplotlib: {e}')


def create_graph(x: Union[np.ndarray, List[Union[int, float]]],
                 y: Union[np.ndarray, List[Union[int, float]]]) -> str:
    """Creates a graph from a list of coordinates."""
    plt.plot(x, y)
    plt.grid(True, linestyle='-.', linewidth=0.5)

    # Save the graph image to a file.
    f = Path.cwd() / 'tmp' / f'{gen_filename()}.png'
    plt.savefig(f)

    # Clearing the graph so the next one doesn't have previously graphed info.
    plt.clf()

    return str(f)


def create_graph_from_expression(expression: str, domain: Optional[List[Union[int, float]]] = None) -> str:
    """
    Uses SymPy and MatPlotLib to create a graph from an expression.

    Dynamic numpy.arange by getting difference in domain and dividing by like 50.
    """
    # Removing the whitespace
    expression = re.sub(re.compile(r'\s+'), '', expression)

    # Creating the modifiable expression.
    expression = sympify(expression)

    # There will only be one variable.
    symbol = symbols('x')

    domain = domain if domain else (-10, 10)

    # Dynamic domain, 50 steps between domain numbers.
    x = np.arange(*domain, sum((abs(domain[0]), domain[1])) / 50)

    # Creating the y values.
    y = [expression.subs(symbol, i) for i in x]

    return create_graph(x, y)
