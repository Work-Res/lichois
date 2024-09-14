import logging

from citizenship.models import ScoreSheet

logger = logging.getLogger(__name__)


class DataGeneratorException(Exception):
    pass


class DataGenerator:
    def __init__(self, scoresheet):
        self.scoresheet = scoresheet

    def generate_data(self):
        try:
            data = [("Category", "Marks", "Marks Scored", "Comments")]
            for response in self.scoresheet.aggregated:
                data.append((response.text, response.marks_range, str(response.score), response.response))
            logger.info(f"Generated data for scoresheet {self.scoresheet.id}")
            return data
        except Exception as e:
            logger.exception(f"Error generating data for scoresheet {self.scoresheet.id}: {e}")
            raise DataGeneratorException(f"Error generating data for scoresheet {self.scoresheet.id}: {e}")
