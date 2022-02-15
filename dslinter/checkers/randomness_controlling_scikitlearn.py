"""Checker which checks rules for controlling randomness."""
from typing import List
import traceback
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from dslinter.util.exception_handler import ExceptionHandler
from dslinter.util.resources import Resources


class RandomnessControllingScikitlearnChecker(BaseChecker):
    """Checker which checks rules for controlling randomness."""

    __implements__ = IAstroidChecker

    name = "randomness-controlling-scikitlearn"
    priority = -1
    msgs = {
        "W5506": (
            "'random_state=None' shouldn't be used in estimators or "
            "cross-validation splitters, it indicates improper randomness control",
            "controlling_randomness_scikitlearn",
            "For reproducible results across executions, remove any use of random_state=None."
        ),
    }
    options = ()

    SPLITTER_FUNCTIONS: List[str] = [
        "make_classification",
        "check_cv",
        "train_test_split",
    ]

    SPLITTER_CLASSES = [
        "GroupKFold",
        "GroupShuffleSplit",
        "KFold",
        "LeaveOneGroupOut",
        "LeavePGroupsOut",
        "LeaveOneOut",
        "LeavePOut",
        "PredefinedSplit",
        "RepeatedKFold",
        "RepeatedStratifiedKFold",
        "ShuffleSplit",
        "StratifiedKFold",
        "StratifiedShuffleSplit",
        "TimeSeriesSplit"
    ]

    estimators_all = Resources.get_hyperparameters()

    def visit_call(self, node: astroid.Call):
        """
        When a Call node is visited, check whether it violated the rules in this checker.

        :param node: The node which is visited.
        """

        try:
            if (
                # pylint: disable = R0916
                hasattr(node, "func")
                and hasattr(node, "keywords")
                and hasattr(node.func, "name")
                and (node.func.name in self.SPLITTER_FUNCTIONS
                     or node.func.name in self.SPLITTER_CLASSES
                     or node.func.name in self.estimators_all)
            ):
                if node.keywords is not None:
                    has_random_state_keyword = False
                    for keyword in node.keywords:
                        if keyword.arg == "random_state":
                            has_random_state_keyword = True
                            if keyword.value.as_string() == "None":
                                self.add_message("controlling_randomness_scikitlearn", node=node)
                    if has_random_state_keyword is False:
                        self.add_message("controlling_randomness_scikitlearn", node=node)
                if node.keywords is None:
                    self.add_message("controlling_randomness_scikitlearn", node=node)

        # pylint: disable = W0702
        except:
            ExceptionHandler.handle(self, node)
            traceback.print_exc()