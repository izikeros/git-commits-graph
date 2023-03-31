from unittest.mock import patch

from conftest import get_freqtrade_commits
from git_commits_graph.main import git_graph

# read commits from file
CHANGES = get_freqtrade_commits()
CHANGES.set_index("date", inplace=True)


class TestGitGraphLines:
    def setup_class(self):
        self.git_dir = "../"
        # self.git_dir = "/Users/krystian.safjan/projects/priv/coin_commander"
        # self.git_dir = "/Users/krystian.safjan/dotfiles"
        # self.git_dir = "/Users/krystian.safjan/projects/priv/freqtrade"
        # self.git_dir = "/Users/krystian.safjan/projects/priv/git-commits-graph"
        # self.git_dir = "/Users/krystian.safjan/projects/ext/bt"

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__defaults(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, total_lines=True)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__log_scale(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, total_lines=True, log_scale=True)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__linear(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, total_lines=True, log_scale=False)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__linear_agg_none(self, mock_fetch_commits):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by=None
        )

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test_total_lines__linear_agg_day(self, mock_fetch_commits):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="D"
        )

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test_total_lines__linear_agg_week(self, mock_fetch_commits):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="W"
        )

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test_total_lines__linear_agg_month(self, mock_fetch_commits):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="M"
        )


class TestGitGraphChanges:
    def setup_class(self):
        # self.git_dir = '../'
        # self.git_dir = "/Users/krystian.safjan/projects/priv/coin_commander"
        self.git_dir = "/Users/krystian.safjan/dotfiles"
        # self.git_dir = "/Users/krystian.safjan/projects/priv/freqtrade"
        # self.git_dir = "/Users/krystian.safjan/projects/priv/git-commits-graph"
        # self.git_dir = "/Users/krystian.safjan/projects/ext/bt"

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__defaults(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_none(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by=None)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_day(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="D")

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_week(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="W")

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_week__logscale(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="W", log_scale=True)

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_month(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="M")

    @patch("git_commits_graph.main.fetch_commits", return_value=CHANGES)
    def test__agg_month__logscale(self, mock_fetch_commits):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="M", log_scale=True)
