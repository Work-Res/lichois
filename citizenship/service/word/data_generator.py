import logging

from citizenship.models import ScoreSheet

logger = logging.getLogger(__name__)


class DataGeneratorException(Exception):
    pass


class DataGenerator:
    def __init__(self, scoresheet):
        self.scoresheet = scoresheet

    def fetch_responses(self):
        try:
            responses = ScoreSheet.objects.filter(scoresheet=self.scoresheet)
            logger.info(f"Fetched {responses.count()} responses for scoresheet {self.scoresheet.id}")
            return responses
        except Exception as e:
            logger.exception(f"Error fetching responses for scoresheet {self.scoresheet.id}: {e}")
            raise

    def generate_data(self):
        try:
            responses = self.fetch_responses()
            data = [("Category", "Marks", "Marks Scored", "Comments")]
            for response in responses:
                data.append((response.text, response.marks_range, str(response.score), response.response))
            logger.info(f"Generated data for scoresheet {self.scoresheet.id}")
            return data
        except Exception as e:
            logger.exception(f"Error generating data for scoresheet {self.scoresheet.id}: {e}")
            raise DataGeneratorException(f"Error generating data for scoresheet {self.scoresheet.id}: {e}")
