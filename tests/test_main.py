from git_commits_graph.main import git_graph


class TestGitGraphLines:
    def setup_class(self):
        # self.git_dir = '../'
        self.git_dir = "/Users/krystian.safjan/projects/priv/coin_commander"
        # self.git_dir = "/Users/krystian.safjan/dotfiles"

    def test__defaults(self):
        git_graph(git_dir=self.git_dir, total_lines=True)

    def test__log_scale(self):
        git_graph(git_dir=self.git_dir, total_lines=True, log_scale=True)

    def test__linear(self):
        git_graph(git_dir=self.git_dir, total_lines=True, log_scale=False)

    def test__linear_agg_none(self):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by=None
        )

    def test_total_lines__linear_agg_day(self):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="D"
        )

    def test_total_lines__linear_agg_week(self):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="W"
        )

    def test_total_lines__linear_agg_month(self):
        git_graph(
            git_dir=self.git_dir, total_lines=True, log_scale=False, aggregate_by="M"
        )


class TestGitGraphChanges:
    def setup_class(self):
        # self.git_dir = '../'
        self.git_dir = "/Users/krystian.safjan/projects/priv/coin_commander"

    def test__defaults(self):
        git_graph(git_dir=self.git_dir, changes=True)

    def test__agg_none(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by=None)

    def test__agg_day(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="D")

    def test__agg_week(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="W")

    def test__agg_week__logscale(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="W", log_scale=True)

    def test__agg_month(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="M")

    def test__agg_month__logscale(self):
        git_graph(git_dir=self.git_dir, changes=True, aggregate_by="M", log_scale=True)
