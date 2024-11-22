
import astroid
import logging
import pandas as pd
from collections.abc import Mapping
from typing import Tuple

from dslinter.checkers.dataset_api_conflict.data_loaders.supported import SUPPORTED
from dslinter.checkers.dataset_api_conflict.util import get_function_id_from_call
from dslinter.checkers.dataset_api_conflict.properties.dataset_properties import DatasetProperties


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DatasetAndProperties = Tuple[pd.DataFrame, DatasetProperties] | None

class DatasetTracker:
    """
    Tracks and manages datasets defined in the code during AST analysis.
    It maintains an internal registry of datasets and provides functionality to add and manage them.
    """

    def __init__(self):
        self._datasets: Mapping[str, pd.DataFrame] = dict()
        self._properties: Mapping[str, DatasetProperties] = dict()

    def add_dataset_from_assign(self, assign_node: astroid.Assign) -> bool:
        """
        Analyzes an assignment node to determine if it represents a dataset and adds it to the internal dataset tracker.

        This method inspects an `astroid.Assign` node to check whether it corresponds to a dataset. If the dataset is identified,
        it updates the relevant internal structures and returns `True`. Otherwise, it returns `False`.

        Args:
            assign_node (astroid.Assign): 
                The assignment node from the Abstract Syntax Tree (AST) to be analyzed. This node represents an assignment
                operation in the code.

        Returns:
            bool: 
                `True` if the assignment node is identified and successfully added as a dataset, `False` otherwise.
        """
        source_node = assign_node.value

        # NOTE: I assume the target is one element of type AssignName.
        dataset_name = assign_node.targets[0].name

        # NOTE: I assume the same name is not used twice. This is unreasonable.
        if dataset_name in self._datasets:
            return False
        
        if isinstance(source_node, astroid.Call):
            dataset_and_properties = self._get_dataset_from_call(source_node)
        elif isinstance(source_node, astroid.Subscript):
            dataset_and_properties = self._get_dataset_from_subscript(source_node)
        else:
            return False
        
        if dataset_and_properties is None:
            return False

        dataset, properties = dataset_and_properties
        dataset = sample_dataset(dataset)
        properties.set_name(dataset_name)

        self._datasets[dataset_name] = dataset
        self._properties[dataset_name] = properties

        properties['min']

        return True
    
    def _get_dataset_from_call(self, call_node: astroid.Call) -> DatasetAndProperties:
        func_id = get_function_id_from_call(call_node)
        
        if not func_id in SUPPORTED:
            logger.debug(f"Unsupported function id '{func_id}'")
            return None

        load_dataset = SUPPORTED[func_id]
        dataset = load_dataset(call_node)
        properties = DatasetProperties(dataset)

        return dataset, properties

    def _get_dataset_from_subscript(self, subscript_node: astroid.Subscript) -> DatasetAndProperties:
        # TODO: This should be separated as much as possible from this class. 
        # NOTE: I assume we subscript on a previously used dataset.
        # NOTE: This does not account for dataframe -> series transformations.
        source_name = subscript_node.value.name
        if source_name not in self._datasets:
            return None
        other_dataset = self._datasets[source_name]
        # NOTE: This currently ignores iloc etc. assignments.
        # NOTE: This currently ignores indexing rows.
        columns = [ele.value for ele in subscript_node.slice.elts]
        other_properties = self.get_properties_of(source_name)
        dataset = other_dataset[columns]
        properties = DatasetProperties(dataset)
        properties.inherit_from(columns, other_properties)
        return dataset, properties


    def get_properties_of(self, dataset_name: "astroid.Name | str") -> "DatasetProperties | None":
        """
        Retrieve the properties associated with a given dataset name.

        Args:
            dataset_name (astroid.Name | str): The name of the dataset for which 
                properties are to be fetched. This can be either an `astroid.Name` 
                object or a string representing the dataset name.

        Returns:
            PropertySet|None: A `PropertySet` object containing the dataset's 
                properties if found, or `None` if the dataset does not exist 
                or has no associated properties.

        Raises:
            TypeError: If `dataset_name` is neither an `astroid.Name` nor a `str`.
        """
        if not isinstance(dataset_name, (str, astroid.Name)):
            raise TypeError("Provided dataset_name is not of type str or astroid.Name.")
        
        if isinstance(dataset_name, astroid.Name):
            dataset_name = dataset_name.name

        if dataset_name in self._properties:
            return self._properties[dataset_name]
        return None


def sample_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    # TODO: get number/setting from the pylint config instead of hardcoding.
    SAMPLE_SIZE = 385
    rows, _ = dataset.shape
    sample_size = min(rows, SAMPLE_SIZE)
    dataset = dataset.sample(sample_size, replace=False, random_state=0)
    return dataset

