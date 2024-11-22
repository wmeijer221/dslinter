"""
Stores the supported data loading methods.
"""

import astroid
from collections.abc import Mapping, Callable
import pandas as pd

from dslinter.checkers.dataset_api_conflict.data_loaders.pandas import pandas_read_csv

SUPPORTED: Mapping[str, Callable[[astroid.Call], pd.DataFrame]] = {
    'pandas.read_csv': pandas_read_csv
}
