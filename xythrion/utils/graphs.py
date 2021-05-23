import asyncio
import functools
from io import BytesIO
from typing import Any, Callable

import numpy as np
from loguru import logger as log

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except (ImportError, ImportWarning) as error:
    log.error("Error when importing Matplotlib.", exc_info=(type(error), error, error.__traceback__))


def plot_and_save(func: Callable) -> Any:
    """Executor wrapper for different synchronous functions."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        return asyncio.get_event_loop().run_in_executor(func, *args, **kwargs)

    return wrapper


@plot_and_save
def graph_2d(x: np.ndarray, y: np.ndarray) -> BytesIO:
    """Graphing points and saving said graph to a file."""
    buffer = BytesIO()
    fig, axis = plt.subplots()

    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    axis.grid(True, linestyle="-.", linewidth=0.5)

    axis.spines["left"].set_position("zero")
    axis.spines["right"].set_color("none")
    axis.spines["bottom"].set_position("zero")
    axis.spines["top"].set_color("none")

    axis.plot(x, y)

    fig.savefig(buffer, format="png")

    return buffer
