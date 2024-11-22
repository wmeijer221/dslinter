import astroid
from collections.abc import Mapping, Callable

from dslinter.checkers.dataset_api_conflict.data_context import DatasetTracker
from dslinter.checkers.dataset_api_conflict.api_contracts.sklearn_svc import sklearn_svm_SVC_fit

SUPPORTED: Mapping[str, Callable[[astroid.Call, DatasetTracker], bool]] = {
    'sklearn.svm.SVC.fit': sklearn_svm_SVC_fit
}
