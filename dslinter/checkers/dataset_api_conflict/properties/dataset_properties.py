import pandas as pd
from collections.abc import Mapping, Iterable

from dslinter.checkers.dataset_api_conflict.properties.supported import SUPPORTED

class DatasetProperties:
    def __init__(self, dataset: pd.DataFrame, name: "str | None" = None):
        self._dataset = dataset
        self._name = name
        self._dataset_properties: Mapping[str, pd.Series] = dict()

    def __getitem__(self, key: str) -> pd.Series:
        if key in self._dataset_properties:
            return self._dataset_properties[key]
        if not key in SUPPORTED:
            raise KeyError("Requested unsupported property %s".format(key))
        calculate_property = SUPPORTED[key]
        prop = calculate_property(self._dataset)
        self._dataset_properties[key] = prop
        return prop

    def __iter__(self):
        return iter(self._dataset_properties)
    
    def __len__(self):
        return len(self._dataset_properties)
    
    def __str__(self):
        return "<DatasetProperties.{}: [{}]>".format(self._name, ", ".join(self._dataset_properties.keys()))

    def inherit_from(self, inherited_columns: Iterable[str], other: "DatasetProperties") -> None:
        """
        Inherits specified properties from another dataset.
        This method updates the current dataset's properties by inheriting selected column attributes from 
        another `DatasetProperties` instance.

        Args:
            inherited_columns (Iterable[str]): 
                A collection of column names to inherit properties for. Only these columns will be updated.
            other (DatasetProperties): 
                Another instance of `DatasetProperties` from which the column properties will be inherited.

        Returns:
            None: 
                This method modifies the current instance in place.

        Raises:
            KeyError: If any of the specified `inherited_columns` are not present in the `other` instance.
            TypeError: If `inherited_columns` is not an iterable or `other` is not a `DatasetProperties` instance.
        """
        for key, value in other._dataset_properties.items():
            copied_values = value[inherited_columns]
            # NOTE: Not sure if this should be a proper copy or if this is okay.
            self._dataset_properties[key] = copied_values

    def set_name(self, name: str) -> None:
        """
        Sets the name of the dataset.

        This method assigns a new name to the dataset, updating its internal metadata. The name is 
        typically used for identification and display purposes.

        Args:
            name (str): 
                The new name to assign to the dataset.

        Returns:
            None: 
                This method modifies the current instance in place.

        Raises:
            ValueError: If the dataset already has a name assigned.
        """
        if not self._name is None:
            raise ValueError("You cannot set `name` twice")
        self._name = name
        