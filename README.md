# Git commits graph
![](https://img.shields.io/pypi/v/git-commits-graph.svg)
![](https://img.shields.io/pypi/pyversions/git-commits-graph.svg)
![](https://img.shields.io/pypi/l/fgit-commits-graph.svg)
![](https://img.shields.io/pypi/dm/git-commits-graph.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/izikeros/git-commits-graph/main.svg)](https://results.pre-commit.ci/latest/github/izikeros/git-commits-graph/main)
[![Maintainability](https://api.codeclimate.com/v1/badges/081a20bb8a5201cd8faf/maintainability)](https://codeclimate.com/github/izikeros/git-commits-graph/maintainability)

Display plot of changes in repo - count of lines or changed lines

## Installation

Use pip to install the package:
```sh
$ pip3 install git-commits-graph
```
or pipx to install in isolated environment:
```sh
$ pipx install git-commits-graph
```

## Usage
plot timeline of both added and removed lines in your repo:
```sh
$ git-commits-graph your-repo-path -c
```
![changes](https://github.com/izikeros/git-commits-graph/raw/main/changes.jpg)

plot lines count evolution in time.
```shell
$ git-commits-graph your-repo-path -t
```
![lines](https://github.com/izikeros/git-commits-graph/raw/main/lines.jpg)
to see all options:
```
$ git-commits-graph --help
```

```
Usage: git-commits-graph [OPTIONS] GIT_DIR

  Plot git commits timeline main function.

Options:
  -b, --branch TEXT               git repository branch to browse.
  -s, --style TEXT                matplotlib plotting style to use.
  -c, --changes                   plot timeline of both added and removed
                                  lines.
  -t, --total-lines               plot lines count time evolution.
  -g, --aggregate-by TEXT         aggregate by: Y - year, M - month, W - week,
                                  D - day
  -l, --log-scale                 aggregate by day
  -a, --list-available-plot-styles
                                  list available plot styles and exit.
  -e, --engine TEXT               plotting engine to use (matplitlib | plotly)
  -o, --output-file TEXT          output file name (for plotly backend)
  --help                          Show this message and exit.

```


## Related Projects
[danielfleischer/git-commits-lines-graph](https://github.com/danielfleischer/git-commits-lines-graph) - A small python script to visualize the number of lines in a project, as a function of time.

## License

[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).
