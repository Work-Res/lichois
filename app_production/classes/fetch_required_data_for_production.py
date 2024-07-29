from app_checklist.utils import ReadJSON
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class FetchRequiredDataForProduction:
    """
    Responsible for pulling required data for production based on configuration.
    """
    def __init__(self, configuration_file_name: str, document_number: str):
        self.configuration_file_name = configuration_file_name
        self.document_number = document_number
        self.data = []

    def read_configuration(self):
        """
        Reads JSON configuration for a particular process.
        Returns:
            dict: The parsed JSON configuration.
        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the JSON is invalid.
        """
        try:
            read_json = ReadJSON(file_location=self.configuration_file_name)
            model_configuration = read_json.json_data()
            return model_configuration
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {self.configuration_file_name}") from e
        except ValueError as e:
            raise ValueError(f"Invalid JSON format in configuration file: {self.configuration_file_name}") from e

    def fetch_required_data(self):
        """
        Fetches the required data for the specified document number based on configuration.
        Raises:
            ObjectDoesNotExist: If the model object does not exist.
            MultipleObjectsReturned: If multiple objects are returned for the query.
        """
        try:
            data = self.read_configuration()
            for app_label_model_name, required_fields in data.get("models", {}).items():
                app_label, model_name = app_label_model_name.split(".")
                model = self.get_model(app_label=app_label, model_name=model_name)
                try:
                    model_object = model.objects.get(document_number=self.document_number)
                except ObjectDoesNotExist:
                    raise ObjectDoesNotExist(
                        f"Object with document number {self.document_number} not found in {model_name}")
                except MultipleObjectsReturned:
                    raise MultipleObjectsReturned(
                        f"Multiple objects found for document number {self.document_number} in {model_name}")

                required_data_result = {
                    "model_obj": model_object,
                    'fields': required_fields
                }
                self.data.append(required_data_result)
        except KeyError as e:
            raise KeyError(f"Configuration file is missing required keys: {e}")

    def get_model(self, app_label: str, model_name: str):
        """
        Retrieves the model class based on app label and model name.
        Args:
            app_label (str): The app label.
            model_name (str): The model name.
        Returns:
            Model: The Django model class.
        Raises:
            ContentType.DoesNotExist: If the ContentType does not exist.
        """
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
            return content_type.model_class()
        except ContentType.DoesNotExist as e:
            raise ContentType.DoesNotExist(f"Model {model_name} in app {app_label} not found") from e

    def get_data(self):
        """
        Public method to initiate data fetching process.
        Returns:
            list: List of dictionaries containing the required data.
        """
        self.fetch_required_data()
        return self.data
