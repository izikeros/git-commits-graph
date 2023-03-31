import math
import os
from typing import Optional

import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import plotly.graph_objs as go
from git_commits_graph.config import FIGSIZE
from git_commits_graph.config import MAX_NUM_BARS
from git_commits_graph.config import XTICKS_FMT
from matplotlib import pyplot as plt


# Define a function to format the y-axis labels
def y_fmt(x, pos):
    if x >= 1000000:
        return f"{x * 1e-6:.0f}M"
    elif x >= 1000:
        return f"{x * 1e-3:.0f}k"
    else:
        return f"{x:.0f}"


# Create a FuncFormatter object from the y_fmt function
y_formatter = ticker.FuncFormatter(y_fmt)


def data_aggregation(aggregate_by, plot_data_add, plot_data_rem):
    if aggregate_by:
        plot_data_add = run_aggregation(plot_data_add, col="added", period=aggregate_by)
        plot_data_rem = run_aggregation(
            plot_data_rem, col="removed", period=aggregate_by
        )
    else:
        for agg in ["D", "W", "M", "Y"]:
            if len(plot_data_add) > MAX_NUM_BARS:
                plot_data_add = run_aggregation(plot_data_add, col="added", period=agg)
                plot_data_rem = run_aggregation(
                    plot_data_rem, col="removed", period=agg
                )
            if len(plot_data_add) <= MAX_NUM_BARS:
                break
    return plot_data_add, plot_data_rem


def plot_changes_px(
    commits,
    git_dir: str,
    log_scale: bool,
    aggregate_by: Optional[str],
    output_file="out.html",
):
    """Plot added/removed lines timeline."""
    plot_data_add = commits.added
    plot_data_rem = commits.removed

    ylabel = "number of lines added/removed"
    if log_scale:
        plot_data_add = (plot_data_add + 1).apply(math.log10)
        plot_data_rem = (plot_data_rem + 1).apply(math.log10)
        ylabel = "log number of lines added/removed"

    plot_data_add, plot_data_rem = data_aggregation(
        aggregate_by=aggregate_by,
        plot_data_add=plot_data_add,
        plot_data_rem=plot_data_rem,
    )

    plot_data_add = pd.DataFrame(plot_data_add)
    plot_data_rem = pd.DataFrame(plot_data_rem)
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plot_data_add.index,
            y=plot_data_add.added,
            name="added",
            marker_color="green",
        )
    )
    fig.add_trace(
        go.Bar(
            x=plot_data_rem.index,
            y=-plot_data_rem.removed,
            name="removed",
            marker_color="red",
        )
    )

    fig.update_layout(
        title=f"Added/Removed Lines in repo {os.path.basename(git_dir)}",
        xaxis_title="Date",
        yaxis_title=ylabel,
    )
    if log_scale:
        fig.update_yaxes(type="log")
    # fig.show()
    fig.write_html(output_file)
    print(f"Saved to {output_file}")


def plot_changes(
    commits, git_dir: str, log_scale: bool, aggregate_by: Optional[str], output_file
):
    """Plot added/removed lines timeline."""
    plot_data_add = commits.added
    plot_data_rem = commits.removed

    ylabel = "number of lines added/removed"
    if log_scale:
        plot_data_add = (plot_data_add + 1).apply(math.log10)
        plot_data_rem = (plot_data_rem + 1).apply(math.log10)
        ylabel = "log number of lines added/removed"

    plot_data_add, plot_data_rem = data_aggregation(
        aggregate_by=aggregate_by,
        plot_data_add=plot_data_add,
        plot_data_rem=plot_data_rem,
    )

    plot_data_add = pd.DataFrame(plot_data_add)
    plot_data_rem = pd.DataFrame(-plot_data_rem)
    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)

    locator = mdates.AutoDateLocator(minticks=3, maxticks=15)
    x_formatter = mdates.ConciseDateFormatter(locator)

    ax = plot_data_add.plot(kind="bar", ax=ax, color="green", label="added")
    ax = plot_data_rem.plot(kind="bar", ax=ax, color="red", label="removed")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(x_formatter)
    ax.yaxis.set_major_formatter(y_formatter)

    plt.xticks(rotation=45)
    format_xticklabels(ax, plot_data_add)
    plt.ylabel(ylabel)

    ax.set_title(f"Added/Removed Lines in repo {os.path.basename(git_dir)}")
    fig.tight_layout()


def plot_total_lines_px(
    commits, git_dir, log_scale, aggregate_by, output_file="out.html"
):
    """Plot total lines timeline."""

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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data.values, mode="lines"))
    fig.update_layout(
        title=f"Number of Lines Progress in repo {os.path.basename(git_dir)}",
        xaxis_title="Date",
        yaxis_title=ylabel,
    )
    fig.update_yaxes(range=[0, 1.1 * plot_data.max()])
    # fig.show()
    fig.write_html(output_file)
    print(f"Saved to {output_file}")


def plot_total_lines(commits, git_dir, log_scale, aggregate_by, output_file):
    """Plot total lines timeline."""
    fig, ax = plt.subplots(1, 1, figsize=[8, 6])

    _delta = commits.delta
    _delta.index = pd.to_datetime(_delta.index, utc=True)
    if aggregate_by:
        _delta = _delta.reset_index()
        _delta = _delta.groupby(pd.Grouper(key="date", axis=0, freq=aggregate_by))[
            "delta"
        ].sum()

    plot_data = _delta.cumsum()

    ylabel = "number of lines"
    if log_scale:
        plot_data = (plot_data + 1).apply(math.log10)
        ylabel = "log number of lines"

    ax = plot_data.plot(ax=ax, kind="line")
    locator = mdates.AutoDateLocator(minticks=10, maxticks=15)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    # ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(ax.xaxis.get_major_locator()))
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(formatter))
    ax.yaxis.set_major_formatter(y_formatter)
    plt.ylabel(ylabel)
    ax.set_title(f"Number of Lines Progress in repo {os.path.basename(git_dir)}")
    ax.set_ylim([0, 1.1 * plot_data.max()])
    # format_xticklabels(ax, plot_data)
    ax.xaxis_date()
    # Optional. Just rotates x-ticklabels in this case.
    fig.autofmt_xdate()
    fig.tight_layout()


def format_xticklabels(ax, plot_data_add, fmt=XTICKS_FMT):
    """Format xticks labels."""
    plot_data_add = plot_data_add.reset_index()
    plot_data_add.date = pd.to_datetime(plot_data_add.date, utc=True)
    plot_data_add["xticks"] = plot_data_add.date.dt.strftime(fmt)
    ax.set_xticklabels(plot_data_add.xticks, rotation=90)


def run_aggregation(plot_data_add, col, period):
    """Aggregate data by period."""
    plot_data_add = plot_data_add.reset_index()
    plot_data_add.date = pd.to_datetime(plot_data_add.date, utc=True)
    plot_data_add = plot_data_add.groupby(pd.Grouper(key="date", axis=0, freq=period))[
        col
    ].sum()
    return plot_data_add
