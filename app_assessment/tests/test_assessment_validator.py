import os

from django.test import TestCase

from app_assessment.models import Assessment
from app_assessment.validators import AssessmentValidator

from app_checklist.utils import ReadJSON


class TestAssessmentValidator(TestCase):

    def setUp(self):

        file_name = "marking_score_work_and_residence.json"
        self.config_location = os.path.join(os.getcwd(), "app_assessment", "data", "assessments", file_name)
        self.assessment = Assessment()
        self.assessment.qualification = 40
        self.assessment.work_experience = 10
        self.assessment.competency = 5
        self.assessment.employer_justification = 20

        reader = ReadJSON(file_location=self.config_location)
        self.validator = AssessmentValidator(
            assessment=self.assessment,
            rules=reader.json_data()
        )

    def test_validate_main_sections_invalid(self):
        self.validator.validate_main_sections()
        self.assertFalse(self.validator.is_valid())
        self.assertGreater(len(self.validator.response.messages), 0)

    def test_validate_main_sections_valid(self):
        self.assessment.qualification = 10
        self.validator.validate_main_sections()
        self.assertTrue(self.validator.is_valid())

    def test_validate_main_sections_valid(self):
        self.assessment.total = 125
        self.assertFalse(self.validator.is_valid())
