"""
Implements the supported data loading methods for the pandas library.
"""

import astroid
import pandas as pd

def pandas_read_csv(call_node: astroid.Call) -> pd.DataFrame:
    """Loads the df using pandas load_csv"""
    # NOTE: At this point, I assume everything that's entered is a constant primitive.
    args = [arg.value for arg in call_node.args]
    kwargs = {kw.arg: kw.value.value for kw in call_node.keywords}
    df = pd.read_csv(*args, **kwargs)
    return df
