from typing import Any, Dict


class DataHelper:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set_field_value(self, data_object: Any, field_name: str) -> None:
        """
        Sets the value of the specified field from the data object into the internal dictionary.

        Args:
            data_object (Any): The object from which to get the field value.
            field_name (str): The name of the field to retrieve and store.
        """
        if data_object:
            if hasattr(data_object, field_name):
                return getattr(data_object, field_name)
            else:
                raise AttributeError(f"{data_object} does not have the field '{field_name}'.")

    def add_field(self, field_name: str, field_value: Any) -> None:
        """
        Adds a field and its value to the internal dictionary.

        Args:
            field_name (str): The name of the field.
            field_value (Any): The value of the field.
        """
        self.data[field_name] = field_value

    def remove_field(self, field_name: str) -> None:
        """
        Removes a field from the internal dictionary.

        Args:
            field_name (str): The name of the field to remove.

        Raises:
            KeyError: If the field name is not found in the dictionary.
        """
        try:
            del self.data[field_name]
        except KeyError:
            raise KeyError(f"Field '{field_name}' does not exist in the data.")

    def get_field(self, field_name: str) -> Any:
        """
        Retrieves the value of a field from the internal dictionary.

        Args:
            field_name (str): The name of the field to retrieve.

        Returns:
            Any: The value of the field.

        Raises:
            KeyError: If the field name is not found in the dictionary.
        """
        try:
            return self.data[field_name]
        except KeyError:
            raise KeyError(f"Field '{field_name}' does not exist in the data.")
