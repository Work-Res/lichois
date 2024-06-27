
import os
from django.test import TestCase
from unittest.mock import patch
from datetime import date

from ..classes import WorkAndResidenceQualificationCriteria, AssessmentHandler
from ..signals import run_assessment_calculation


from app.models import Application, ApplicationDocument, ApplicationUser, ApplicationStatus
from app_checklist.classes import CreateChecklistService
from ..classes.assessment_evaluator import AssessmentEvaluator
from ..models import AssessmentResult


class TestAssessmentHandler(TestCase):

    def setUp(self):

        file_name = "new_work_and_residence.json"
        self.config_location = os.path.join(os.getcwd(), "app_assessment", "data", "assessments", file_name)
        self.custom_criteria = WorkAndResidenceQualificationCriteria(
            setswana=True,
            english=False,
            competency=False,
            degree=False,
            masters=False,
            doctorate=False,
            diploma=False,
            certifications=False,
            certificate=False,
            employer_justification=False,
            scarce_skill=False,
            less_than_or_equal_five_years=False,
            six_to_ten_years=False,
            eleven_to_twenty_years=False,
            greater_than_twenty_one_years=False,
            maximum_points=120,
            pass_mark=60
        )

    def test_calculated_score(self):
        """Checks the total if all attributes are captured.
        """
        assessment_handler = AssessmentHandler(
            assessment_rules_file_location_name=self.config_location,
            source=self.custom_criteria,
            document_number="test-doc"
        )
        self.assertEqual(assessment_handler.calculated_score(), 10)

    def test_totals(self):
        """Checks the total if all attributes are captured.
        """
        self.custom_criteria.english = True
        assessment_handler = AssessmentHandler(
            assessment_rules_file_location_name=self.config_location,
            source=self.custom_criteria,
            document_number="test-doc"
        )
        self.assertEqual(assessment_handler.calculated_score(), 20)


    def test_total_with_more_options(self):
        """Checks the total if all attributes are captured.
        """
        self.custom_criteria.english = False
        self.custom_criteria.setswana = True
        self.custom_criteria.eleven_to_twenty_years = True
        assessment_handler = AssessmentHandler(
            assessment_rules_file_location_name=self.config_location,
            source=self.custom_criteria,
            document_number="test-doc"
        )
        self.assertEqual(assessment_handler.calculated_score(), 40)

    def test_total_with_more_options_1(self):
        """Checks the total if all attributes are captured.
        """
        self.custom_criteria.english = False
        self.custom_criteria.setswana = True
        self.custom_criteria.eleven_to_twenty_years = True
        assessment_handler = AssessmentHandler(
            assessment_rules_file_location_name=self.config_location,
            source=self.custom_criteria,
            document_number="test-doc"
        )
        self.assertEqual(assessment_handler.calculated_percent(), 33.33)

    def test_total_with_more_options_2(self):
        """Checks the total if all attributes are captured.
        """
        self.custom_criteria.english = False
        self.custom_criteria.setswana = True
        self.custom_criteria.eleven_to_twenty_years = True
        assessment_handler = AssessmentHandler(
            assessment_rules_file_location_name=self.config_location,
            source=self.custom_criteria,
            document_number="test-doc"
        )
        self.assertEqual(assessment_handler.calculated_percent(), 33.33)