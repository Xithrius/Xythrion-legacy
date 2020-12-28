import logging
from io import BytesIO
from tempfile import TemporaryFile
from typing import List, Optional, TypeVar, Union

import numpy as np
from discord import File
from discord.ext.commands import Context
from matplotlib.pyplot import Axes, Figure

from .shortcuts import DefaultEmbed

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.style.use("dark_background")

except Exception as e:
    log.error("Error when importing Matplotlib.", exc_info=(type(e), e, e.__traceback__))

_N = TypeVar("_N", int, float)
NUMBER_ARRAY = List[Union[_N]]
ANY_NUMBER_ARRAY = Union[np.ndarray, NUMBER_ARRAY]


def check_2d(lst: ANY_NUMBER_ARRAY) -> bool:
    """Checks if all items in a 2d list are lists."""
    return all((isinstance(item, list) for item in lst))


class Graph:
    """Graphing plot(s) within one image."""

    def __init__(
        self,
        ctx: Context,
        buffer: TemporaryFile,
        x: Optional[Union[ANY_NUMBER_ARRAY, List[ANY_NUMBER_ARRAY]]] = None,
        y: Optional[Union[ANY_NUMBER_ARRAY, List[ANY_NUMBER_ARRAY]]] = None,
        *,
        fig: Optional[Figure] = None,
        ax: Optional[Union[Axes, List[Axes]]] = None,
        x_labels: Union[str, List[str]] = "x",
        y_labels: Union[str, List[str]] = "y",
    ) -> None:
        self.ctx = ctx
        self.buffer = buffer

        self.x = x
        self.y = y

        if fig is None and ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig = fig
            self.ax = ax

        self.fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

        if isinstance(self.ax, list) and self.ax:
            for i, axis in enumerate(self.ax):
                axis.grid(True, linestyle="-.", linewidth=0.5)

                if all((x[i].any(), y[i].any())):
                    axis.plot(x[i], y[i])

                axis.set_xticklabels(x_labels[i])
                axis.set_yticklabels(y_labels[i])

        else:
            self.ax.grid(True, linestyle="-.", linewidth=0.5)

            self.ax.spines["left"].set_position("zero")
            self.ax.spines["right"].set_color("none")
            self.ax.spines["bottom"].set_position("zero")
            self.ax.spines["top"].set_color("none")

            if all((x.any(), y.any())):
                self.ax.plot(x, y)

            self.ax.set_xticklabels(x_labels)
            self.ax.set_yticklabels(y_labels)

        self.fig.savefig(self.buffer, format="png")
        self.buffer.seek(0)

    def __enter__(self) -> DefaultEmbed:
        buffer = BytesIO(self.buffer.read())

        file = File(fp=buffer, filename="temporary_graph_file.png")

        return DefaultEmbed(self.ctx, embed_attachment=file)

    def __exit__(self, *args) -> None:
        self.fig.clear()

        if isinstance(self.ax, list):
            for axis in self.ax:
                axis.clear()

        else:
            self.ax.clear()
