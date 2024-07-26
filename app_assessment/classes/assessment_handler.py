import logging

from datetime import date

from typing import Dict

from app_assessment.models import Assessment
from .assessment_evaluator import AssessmentEvaluator
from app_checklist.utils import ReadJSON
from ..models.assessment_result import AssessmentResult


class AssessmentHandler:

    def __init__(self, assessment_rules_file_location_name: str, source, document_number: str,
                 assessment: Assessment = None):
        """
        Initializes the AssessmentHandler with the given parameters.
            :param assessment_rules_file_location_name: Location of the assessment rules JSON file.
            :param source: The source data for the assessment.
            :param document_number: The document number associated with the assessment.
        """
        self.assessment_rules_file_name = assessment_rules_file_location_name
        self.source = source
        self.document_number = document_number
        self.evaluator = None
        self.logger = logging.getLogger(__name__)
        self._rules = {}
        self.assessment = assessment

    def rules(self) -> Dict:
        """
        Reads and returns the assessment rules from a JSON file.

        :return: The assessment rules as a dictionary.
        """
        try:
            reader = ReadJSON(file_location=self.assessment_rules_file_name)
            self.logger.info("Successfully read rules from JSON file: %s", self.assessment_rules_file_name)
            return reader.json_data()
        except Exception as e:
            self.logger.error(f"Error reading rules from JSON file: {e}")
            return {}

    def calculated_score(self) -> float:
        """
        Calculates the assessment score based on the source data and rules.
        :return: The calculated score.
        """
        try:
            self._rules = self.rules()
            if not self._rules:
                self.logger.warning("No rules found. Returning score 0.0")
                return 0.0

            self.evaluator = AssessmentEvaluator(source=self.source, rules=self._rules)
            self.evaluator.evaluate()
            score = self.evaluator.calculate_score()
            self.logger.info("Calculated score: %f", score)
            return score
        except Exception as e:
            self.logger.error("Error calculating score: %s", e)
            return 0.0

    def calculated_percent(self):
        score = self.calculated_score()
        marks = (score / self.source.maximum_points) * 100
        return round(marks, 2)

    def calculated_passed(self):
        if int(self.calculated_percent()) > int(self.source.pass_mark):
            return True
        return False

    def create_assessment_results(self) -> None:
        """
        Creates and saves the assessment results to the database.
        :return: None
        """
        try:
            self.evaluator.assessment_results.update({
                "calculated_score": self.calculated_score(),
                "calculated_pass": self.calculated_passed(),
                "calculated_marks_in_percent": self.calculated_percent(),
                "applied_business_criteria": self._rules
            })
            if self.evaluator is not None:
                AssessmentResult.objects.create(
                    document_number=self.document_number,
                    score=self.calculated_score(),
                    output_results=self.evaluator.assessment_results,
                    result_date=date.today()
                )
                self.logger.info("Assessment results created successfully for document_number: %s",
                                 self.document_number)
            else:
                self.logger.warning("Evaluator is not initialized. Assessment results not created.")
        except Exception as e:
            self.logger.error("Error creating assessment results: %s", e)
