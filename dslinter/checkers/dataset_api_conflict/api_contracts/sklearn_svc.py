"""
Implements the supported contracts for the sklearn.svc library.
"""

import astroid

from dslinter.checkers.dataset_api_conflict.data_context import DatasetTracker
from dslinter.checkers.dataset_api_conflict.api_contracts.simple_rules import scale_is_equal, range_is_equal
from dslinter.checkers.dataset_api_conflict.util import build_kwargs

def sklearn_svm_SVC_fit(call_node: astroid.Call, context: DatasetTracker) -> bool:
    # TODO: There has to be a better way than this. This is unmaintainable.
    keys = ["X", "y", "sample_weight"]
    kwargs = build_kwargs(call_node, keys)
    dataset = kwargs['X']
    preconditions = [range_is_equal, scale_is_equal]
    preconditions_met = all(p(dataset, context) for p in preconditions)
    return preconditions_met
