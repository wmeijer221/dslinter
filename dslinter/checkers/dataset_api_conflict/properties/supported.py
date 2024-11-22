"""
Stores the supported property calculations.
"""

import numpy as np
import pandas as pd
from collections.abc import Mapping, Callable

SUPPORTED: Mapping[str, Callable[[pd.DataFrame], pd.Series]] = {
    'min': lambda ds: ds.min(),
    'max': lambda ds: ds.max(),
    'mean': lambda ds: ds.mean(),
    'mean': lambda ds: ds.median(),
    'stddev': lambda ds: ds.std(),
    'l2_norms': lambda ds: np.linalg.norm(ds, axis=0)
}
