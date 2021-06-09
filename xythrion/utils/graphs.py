import asyncio
import functools
from io import BytesIO
from typing import Any, Callable, Union

import numpy as np
from loguru import logger as log

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as e:
    log.error("Error when importing Matplotlib.", exc_info=(type(e), e, e.__traceback__))


def plot_and_save(func: Callable) -> Any:
    """Executor wrapper for different synchronous functions."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        sync_func = functools.partial(func, *args, **kwargs)

        return await asyncio.get_event_loop().run_in_executor(None, sync_func)

    return wrapper


@plot_and_save
def graph_2d(
    x: Union[np.ndarray, list],
    y: Union[np.ndarray, list],
    *,
    graph_type: str = "line",
    autorotate_xaxis: bool = True
) -> BytesIO:
    """Graphing points and saving said graph to a file."""
    buffer = BytesIO()
    fig, axis = plt.subplots()

    axis.grid(True, linestyle="-.", linewidth=0.5)

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
