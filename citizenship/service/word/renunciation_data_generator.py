import json
import logging


class DataGeneratorException(Exception):
    pass


logger = logging.getLogger(__name__)


class DataGenerator:
    def __init__(self, scoresheet):
        self.scoresheet = scoresheet

    def parse_aggregated_data(self):
        """Parses the aggregated data from the scoresheet and ensures it's in list form."""
        if isinstance(self.scoresheet.aggregated, str):
            try:
                return json.loads(self.scoresheet.aggregated)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON format in scoresheet {self.scoresheet.id}: {e}")
                raise DataGeneratorException(f"Invalid JSON format in scoresheet {self.scoresheet.id}: {e}")
        elif isinstance(self.scoresheet.aggregated, list):
            return self.scoresheet.aggregated
        else:
            logger.error(f"Unsupported data format in scoresheet {self.scoresheet.id}")
            raise DataGeneratorException(f"Unsupported data format in scoresheet {self.scoresheet.id}")

    def generate_data(self):
        """Generates the data based on the scoresheet's aggregated information."""
        try:
            # Initialize data with headers
            data = [("Category", "Marks", "Marks Scored", "Comments")]

            # Parse the aggregated data
            aggregated_data_list = self.parse_aggregated_data()

            # Append the data from aggregated data
            data.extend(
                (item.get("text", "Unknown"),
                 item.get("marks_range", "N/A"),
                 item.get("average_score", "N/A"),
                 "NA")
                for item in aggregated_data_list
            )

            logger.info(f"Successfully generated data for scoresheet {self.scoresheet.id}")
            return data

        except DataGeneratorException as e:
            logger.exception(f"Data generation failed for scoresheet {self.scoresheet.id}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during data generation for scoresheet {self.scoresheet.id}: {e}")
            raise DataGeneratorException(
                f"Unexpected error during data generation for scoresheet {self.scoresheet.id}: {e}")
