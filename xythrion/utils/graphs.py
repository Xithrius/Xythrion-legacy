from io import BytesIO
from typing import Union

import numpy as np
from loguru import logger as log

from xythrion.utils.wrappers import await_sync

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as e:
    log.error("Error when importing Matplotlib.", exc_info=(type(e), e, e.__traceback__))


@await_sync
def graph_2d(
    x: Union[np.ndarray, list],
    y: Union[np.ndarray, list],
    *,
    x_title: str = None,
    y_title: str = None,
    title: str = None,
    graph_type: str = "line",
    grid: bool = True,
    autorotate_xaxis: bool = True
) -> BytesIO:
    """Graphing points and saving said graph to a file."""
    buffer = BytesIO()
    fig, axis = plt.subplots()

    axis.grid(grid, linestyle="-.", linewidth=0.5)

    if not any((x_title, y_title, title)):
        raise ValueError("All titles are required to exist.")

    axis.set_xlabel(x_title)
    axis.set_ylabel(y_title)

    if graph_type == "line":
        axis.plot(x, y)
    elif graph_type == "bar":
        placements = np.linspace(0, len(x) + 1, len(x))
        axis.bar(placements, y, 0.5)
        axis.set_xticks(placements)
        axis.set_xticklabels(x)
    else:
        raise ValueError(f"Invalid graph_type '{graph_type}'.")

    if autorotate_xaxis:
        plt.gcf().autofmt_xdate()

    fig.savefig(buffer, format="png")

    buffer.seek(0)

    return buffer
