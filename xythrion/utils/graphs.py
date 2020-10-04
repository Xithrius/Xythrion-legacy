import logging
from pathlib import Path
from typing import AnyStr, Iterable, List, Optional, Union

import numpy as np
from discord.ext.commands import Context
from matplotlib.pyplot import Axes, Figure

from .shortcuts import DefaultEmbed, gen_filename

log = logging.getLogger(__name__)

try:
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.style.use('dark_background')
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.grid(True, linestyle='-.', linewidth=0.5)

except Exception as e:
    log.critical(f'Error when importing matplotlib: {e}')


class Graph:
    """Getting graphs all over the place."""

    def __init__(
            self,
            ctx: Context,
            x: Optional[Union[np.ndarray, List[Union[int, float]]]] = None,
            y: Optional[Union[np.ndarray, List[Union[int, float]]]] = None,
            *,
            fig: Optional[Figure] = None,
            ax: Optional[Axes] = None,
            x_labels: Optional[Iterable[AnyStr]] = None,
            y_labels: Optional[Iterable[AnyStr]] = None
    ) -> None:
        if not fig and not ax:
            self.fig, self.ax = plt.subplots()

        else:
            self.fig = fig
            self.ax = ax

        if x:
            self.ax.plot(x)

        elif y:
            self.ax.plot(y)

        elif x and y:
            self.ax.plot(x, y)

        if x_labels:
            self.ax.set_xticklabels(x_labels)

        if y_labels:
            self.ax.set_yticklabels(y_labels)

        file = f'{gen_filename()}.png'
        self.save_path = Path.cwd() / 'tmp' / file
        self.fig.savefig(self.save_path, format='png')

        self.embed = DefaultEmbed(ctx, embed_attachment=self.save_path)

        # self.fig.clear()
        # self.ax.clear()
