import math
import os
from typing import Optional

import pandas as pd
from git_commits_graph.config import FIGSIZE
from git_commits_graph.config import XTICKS_FMT
from matplotlib import pyplot as plt


def plot_changes(commits, git_dir: str, log_scale: bool, aggregate_by: Optional[str]):
    plot_data_add = commits.added
    plot_data_rem = commits.removed

    ylabel = "number of lines added/removed"
    if log_scale:
        plot_data_add = (plot_data_add + 1).apply(math.log10)
        plot_data_rem = (plot_data_rem + 1).apply(math.log10)
        ylabel = "log number of lines added/removed"

    if aggregate_by:
        plot_data_add = run_aggregation(plot_data_add, col="added", period=aggregate_by)
        plot_data_rem = run_aggregation(
            plot_data_rem, col="removed", period=aggregate_by
        )

    plot_data_add = pd.DataFrame(plot_data_add)
    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)

    ax = plot_data_add.plot(kind="bar", ax=ax, color="green", label="added")
    ax = (-plot_data_rem).plot(kind="bar", ax=ax, color="red", label="removed")

    # plot xticks (dates)
    format_xticklabels(ax, plot_data_add)
    plt.ylabel(ylabel)
    ax.set_title(f"Added/Removed Lines in repo {os.path.basename(git_dir)}")
    fig.tight_layout()


def plot_total_lines(commits, git_dir, log_scale, aggregate_by):
    fig, ax = plt.subplots(1, 1, figsize=[8, 6])

    _delta = commits.delta
    if aggregate_by:
        _delta = _delta.reset_index()
        _delta.date = pd.to_datetime(_delta.date, utc=True)
        _delta = _delta.groupby(pd.Grouper(key="date", axis=0, freq=aggregate_by))[
            "delta"
        ].sum()

    plot_data = _delta.cumsum()

    ylabel = "number of lines"
    if log_scale:
        plot_data = (plot_data + 1).apply(math.log10)
        ylabel = "log number of lines"

    ax = plot_data.plot()
    plt.ylabel(ylabel)
    ax.set_title(f"Number of Lines Progress in repo {os.path.basename(git_dir)}")
    ax.set_ylim([0, 1.1 * plot_data.max()])
    # format_xticklabels(ax, plot_data)
    ax.xaxis_date()
    # Optional. Just rotates x-ticklabels in this case.
    fig.autofmt_xdate()


def format_xticklabels(ax, plot_data_add, fmt=XTICKS_FMT):
    plot_data_add = plot_data_add.reset_index()
    plot_data_add.date = pd.to_datetime(plot_data_add.date, utc=True)
    plot_data_add["xticks"] = plot_data_add.date.dt.strftime(fmt)
    ax.set_xticklabels(plot_data_add.xticks, rotation=90)


def run_aggregation(plot_data_add, col, period):
    plot_data_add = plot_data_add.reset_index()
    plot_data_add.date = pd.to_datetime(plot_data_add.date, utc=True)
    plot_data_add = plot_data_add.groupby(pd.Grouper(key="date", axis=0, freq=period))[
        col
    ].sum()
    return plot_data_add
