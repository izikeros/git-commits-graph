# project root directory
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent


def get_freqtrade_commits():
    """Get freqtrade commits."""
    return pd.read_csv(PROJECT_ROOT / "tests/fixtures/repo_freqtrade.csv")
