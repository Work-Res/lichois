import json


class ReadJSON:

    def __init__(self, file_location):
        self.file_location = file_location

    def json_data(self):
        with open(self.file_location, 'r') as file:
            # Load JSON data from the file
            return json.load(file)
