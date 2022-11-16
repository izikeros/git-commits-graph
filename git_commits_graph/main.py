import click
import git
import matplotlib.pyplot as plt
import pandas as pd
from git_commits_graph.config import DEFAULT_STYLE
from git_commits_graph.plotters import plot_changes
from git_commits_graph.plotters import plot_total_lines


@click.command()
@click.argument("git_dir", required=True)
@click.option("-b", "--branch", default=None, help="git repository branch to browse.")
@click.option(
    "-s", "--style", default=DEFAULT_STYLE, help="matplotlib plotting style to use."
)
@click.option(
    "-c",
    "--changes",
    is_flag=True,
    help="plot timeline of both added and removed lines.",
)
@click.option(
    "-t", "--total-lines", is_flag=True, help="plot lines count time evolution."
)
@click.option(
    "-g",
    "--aggregate-by",
    help="aggregate by: Y - year, M - month, W - week, D - day",
    default=None,
)
@click.option("-l", "--log-scale", is_flag=True, help="aggregate by day")
@click.option(
    "-a",
    "--list-available-plot-styles",
    is_flag=True,
    help="list available plot styles and exit.",
)
def main(
    git_dir,
    branch,
    total_lines,
    changes,
    log_scale,
    style,
    list_available_plot_styles,
    aggregate_by,
):

    if list_available_plot_styles:
        print(plt.style.available)
        exit()

    git_graph(
        git_dir=git_dir,
        branch=branch,
        total_lines=total_lines,
        changes=changes,
        log_scale=log_scale,
        style=style,
        aggregate_by=aggregate_by,
    )


def git_graph(
    git_dir,
    branch=None,
    total_lines=False,
    changes=False,
    log_scale=False,
    style=DEFAULT_STYLE,
    aggregate_by=None,
):
    # TODO: KS: 2022-06-06: Fetch commits from the github repo without cloning it.
    #       see: https://stackoverflow.com/a/64561416/3247880

    git_dir, repo = get_git_repo(
        changes=changes, git_dir=git_dir, total_lines=total_lines
    )
    commits = fetch_commits(branch, repo)

    plt.style.use(style)
    if total_lines:
        plot_total_lines(
            commits=commits,
            git_dir=git_dir,
            log_scale=log_scale,
            aggregate_by=aggregate_by,
        )
        plt.show()
    if changes:
        plot_changes(
            commits=commits,
            git_dir=git_dir,
            log_scale=log_scale,
            aggregate_by=aggregate_by,
        )
        plt.show()


def get_git_repo(changes, git_dir, total_lines):
    git_dir = git_dir.strip('"').strip("'")
    try:
        repo = git.repo.Repo(git_dir)
    except git.exc.InvalidGitRepositoryError:
        print(f"Not a valid git project directory: {git_dir}")
        exit()
    except git.exc.NoSuchPathError:
        print(f"Directory not exist: {git_dir}")
        exit()
    except git.exc.GitError as ge:
        print(f"Git error: {ge}")
        exit()
    if not any([total_lines, changes]):
        print("You must specify at least one of the options: -t, -c")
        print(
            "Choose -t for total number of lines and/or -c for added and removed lines."
        )
        exit()
    return git_dir, repo


def fetch_commits(branch, repo):
    commits = []
    try:
        for i in reversed(list(repo.iter_commits(rev=branch))):
            stat = i.stats.total
            commits.append(
                [
                    i.committed_datetime.isoformat(),
                    stat["insertions"],
                    stat["deletions"],
                ]
            )
    except git.exc.GitError as ge:
        print(f"Git error: {ge}")
        exit()
    except ValueError as ve:
        print(f"Value error: {ve}")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()

    commits = prepare_commits_dataframe(commits)
    return commits


def prepare_commits_dataframe(commits):
    commits = pd.DataFrame(commits, columns=["date", "added", "removed"])
    commits["delta"] = commits["added"] - commits["removed"]
    commits.date = pd.to_datetime(commits.date)
    commits.set_index(["date"], inplace=True)
    return commits
