import logging
import json


class ReadJSON:
    """
    Read json file given file location.
    """

    def __init__(self, file_location):
        self.logger = logging.getLogger(__name__)
        self.file_location = file_location

    def json_data(self):
        try:
            with open(self.file_location, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.debug(f"Error: The file at {self.file_location} was not found.")
        except PermissionError:
            self.logger.debug(
                f"Error: Permission denied to read the file at {self.file_location}."
            )
        except IsADirectoryError:
            self.logger.debug(
                f"Error: The path {self.file_location} is a directory, not a file."
            )
        except IOError as e:
            self.logger.debug(
                f"Error: An I/O error occurred while reading the file at {self.file_location}: {e}"
            )
