import csv
import logging

logger = logging.getLogger(__name__)


class InterviewResponseImportService:
    """
    Service class for importing interview responses from a CSV file.

    Attributes:
        csv_path (str): The path to the CSV file.
        data (list): List to store the rows read from the CSV file.
    """

    def __init__(self, csv_path):
        """
        Initializes the service with the path to the CSV file.

        Args:
            csv_path (str): The path to the CSV file.
        """
        self.csv_path = csv_path
        self.data = []

    def read_csv(self):
        """
        Reads the CSV file and stores its content in the data attribute.
        """
        try:
            with open(self.csv_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                self.data = [row for row in reader]
                logger.info(f"Read {len(self.data)} rows from {self.csv_path}")
        except FileNotFoundError:
            logger.error(f"File not found: {self.csv_path}")
        except Exception as e:
            logger.exception(f"Unexpected error reading file {self.csv_path}: {e}")
