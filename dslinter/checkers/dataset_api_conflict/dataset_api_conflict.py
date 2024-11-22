import astroid
import logging

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from dslinter.checkers.dataset_api_conflict.data_context import DatasetTracker
from dslinter.checkers.dataset_api_conflict.util import get_function_id_from_call
from dslinter.checkers.dataset_api_conflict.api_contracts.supported import SUPPORTED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatasetApiConflict(BaseChecker):
    __implements__ = IAstroidChecker

    name = "data-api-conflict"
    priority = -1
    msgs = {
        "W5200": (
            "Dataset API conflict.",
            "data-api-conflict",
            "There is a conflict between the used API and the distribution of the inserted data."
        )
    }
    options = ()

    def __init__(self, linter):
        self._data_context = DatasetTracker()
        super().__init__(linter)

    def visit_assign(self, assign_node: astroid.Assign):
        _ = self._data_context.add_dataset_from_assign(assign_node)

    def visit_call(self, call_node: astroid.Call):
        _ = self._handle_function_call(call_node)

    def _handle_function_call(self, call_node: astroid.Call) -> bool:
        func_id = get_function_id_from_call(call_node)

        if func_id not in SUPPORTED:
            logger.debug(f"Unsupported function id '{func_id}'")
            return False

        func = SUPPORTED[func_id]
        is_used_correctly = func(call_node, self._data_context)

        if not is_used_correctly:
            self.add_message(self.name, node=call_node)

        return True
