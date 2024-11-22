"""
Implements a set of basic preconditions that can be reused in other API contracts.
"""

import astroid
import pandas as pd

from dslinter.checkers.dataset_api_conflict.dataset_api_conflict import DatasetTracker

# TODO: Make the threshold configurable.
L2_SCALE_THRESHOLD = 10

def scale_is_equal(dataset: 'str | astroid.Name', context: DatasetTracker) -> bool:
    properties = context.get_properties_of(dataset)
    l2_norms = properties['l2_norms']
    mn = min(l2_norms)
    mx = max(l2_norms)
    ratio = mx / mn
    low_enough = ratio < L2_SCALE_THRESHOLD
    return low_enough

def range_is_equal(dataset: 'str | astroid.Name', context: DatasetTracker) -> bool:
    properties = context.get_properties_of(dataset)
    minima: pd.DataFrame = properties['min']
    same_minimum = all(mn == minima.iloc[0] for mn in minima.iloc[1:])
    maxima: pd.DataFrame = properties['max']
    same_maximum = all(mx == maxima.iloc[0] for mx in maxima.iloc[1:])
    same_range = same_minimum and same_maximum
    return same_range
