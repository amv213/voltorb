import itertools
import os
from collections import defaultdict
from datetime import datetime
from typing import Iterable, Iterator

import attr
import httpx
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import snug
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap
from matplotlib.pyplot import colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
from rich import print

import electron.schemas
from electron import electricity_maps, execute, execute_async, executor, token_auth


def _google_colormap(top_color: str = "green") -> Colormap:
    center = 0.8  # 80% CFE considered "neutral"
    return matplotlib.colors.LinearSegmentedColormap.from_list(
        "mycmap", [(0, "black"), (center, "white"), (1, top_color)], N=1000
    )


def plot_clock(
    hourly_percentages: dict[int, float],
    colormap: Colormap,
    radius: float = 1,
    ax: Axes = None,
) -> Axes:
    _NUM_SLICES = 24
    _SLICE_WIDTH = 2 * np.pi / _NUM_SLICES

    thetas = [i * 2 * np.pi / 24 for i in range(_NUM_SLICES)]
    y = [radius for _ in thetas]

    ax = ax or plt.subplot(111, projection="polar")

    bars = ax.bar([theta + _SLICE_WIDTH / 2 for theta in thetas], y, width=_SLICE_WIDTH)

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim([0, 1])
    ax.set_rorigin(-1 / 10)

    ax.set_xticks(thetas)
    ax.set_xticklabels([i for i in range(_NUM_SLICES)])
    ax.set_yticks([])

    # Colour each slice based on hourly percentages
    for h, bar in enumerate(bars):
        # there might not be data for all hours of the day
        cfe = hourly_percentages.get(h)

        if cfe is None:
            bar.set_visible(False)
        else:
            bar.set_facecolor(colormap(cfe / 100))

    return ax


def colormap_plot(colormap: Colormap, ax=None):
    ax = ax or plt.gca()

    # im = ax.imshow(np.arange(100).reshape((10,10)), cmap=colormap)
    # im.set_visible(False)
    # ax.set_axis_off()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=1, axes_class=Axes)
    plt.colorbar(ScalarMappable(cmap=colormap), cax=cax, orientation="vertical")

    return ax


if __name__ == "__main__":
    sns.set_theme()
    cmap = _google_colormap()
    cmap_b = _google_colormap(top_color="blue")

    load_dotenv()
    API_TOKEN = os.environ.get("API_TOKEN")

    with httpx.Client() as client:
        query = electricity_maps.power_breakdown.get_history("DK")
        power_breakdown_history = execute(
            query, auth=token_auth(API_TOKEN), client=client
        )

    print(power_breakdown_history)

    # bucket power breakdowns into individual days
    power_breakdowns_by_date = itertools.groupby(
        power_breakdown_history.history, key=lambda x: x.datetime.date()
    )
    for date, daily_power_breakdowns in power_breakdowns_by_date:
        daily_power_breakdowns = list(daily_power_breakdowns)

        hourly_fossil_free_energy_percentage = {
            power_breakdown.datetime.hour: power_breakdown.fossil_free_percentage
            for power_breakdown in daily_power_breakdowns
        }
        ax = plot_clock(hourly_fossil_free_energy_percentage, colormap=cmap)
        ax.set_title(f"{date.isoformat()} ({power_breakdown_history.zone})")

        hourly_renewable_energy_percentage = {
            power_breakdown.datetime.hour: power_breakdown.renewable_percentage
            for power_breakdown in daily_power_breakdowns
        }
        ax = plot_clock(
            hourly_renewable_energy_percentage, colormap=cmap_b, radius=0.5, ax=ax
        )

        plt.show()

    # for fossil_free_percentages in daily_datas:
    #    fig = plt.figure()
    # ax1 = plt.subplot(121, projection='polar')

    #    clock_plot(fossil_free_percentages, colormap=cmap)

    #    plt.show()

    """

    data = [[i * 100 / 24 for i in range(24)] for _ in range(365)]

    # sns.set_theme()
    cmap = _get_google_colormap()

    ax = plt.subplot(111)
    img = ax.imshow(np.array(data).T, origin="upper", cmap=cmap)

    ax.set_xticks([])
    ax.set_yticks([i for i in range(24)])
    ax.set_aspect(4)

    plt.colorbar(img, cax=ax, orientation='horizontal')
    """
