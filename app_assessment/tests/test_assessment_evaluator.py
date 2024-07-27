import os
from django.test import TestCase
from unittest.mock import patch
from datetime import date

from ..models.assessment_result import AssessmentResult
from ..signals import run_assessment_calculation


from app.models import Application, ApplicationDocument, ApplicationUser, ApplicationStatus
from app_checklist.classes import CreateChecklistService
from ..classes.assessment_evaluator import AssessmentEvaluator


def application(status):
    try:
        obj = Application.objects.get(application_status__status=status)
        return obj
    except Application.DoesNotExist:
        return None


class SourceModel:

    def __init__(self, qualification, work_experience=None):
        self.qualification = qualification
        self.work_experience = work_experience


class TestAssessmentEvaluator(TestCase):

    def create_data(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklistService()
        create.create(file_location=output_file)

        applicant = ApplicationUser(
            full_name="Test test",
            user_identifier="YYYXXX",
            work_location_code="01",
            dob="2000106")
        application_document = ApplicationDocument(
            id="abc",
            applicant=applicant,
            document_number="WR0001200202",
            signed_date=date.today(),
            submission_customer="test"
        )
        status = ApplicationStatus(id="abcd", code="NEW")
        app = Application(
            id="yze",
            last_application_version_id=1,
            application_document=application_document,
            application_status=status,
            process_name="WORK_RESIDENT_PERMIT"
        )
        return app

    def test_assessment_evaluator_flatten_dict(self):
        expected_dict = {
            'degree': 25, 'diploma': 20, 'certificate': 15, 'greater_than_10_years': 20,
            'greater_than_5_years': 15, 'greater_than_2_years': 10, 'less_than_2_years': 2
        }

        source = SourceModel(
            qualification="degree",
            work_experience="greater_than_2_years"
        )
        rules = {
              "qualification":  {
                "degree": 25,
                "diploma": 20,
                "certificate": 15
              },
              "work_experience": {
                "greater_than_10_years": 20,
                "greater_than_5_years": 15,
                "greater_than_2_years":  10,
                "less_than_2_years": 2
              }
        }
        evaluator = AssessmentEvaluator(source=source, rules=rules)
        evaluator.evaluate()
        self.assertEqual(expected_dict, evaluator.points_list)

    def rules(self):
        return {
              "qualification":  {
                "degree": 25,
                "diploma": 20,
                "certificate": 15
              },
              "work_experience": {
                "greater_than_10_years": 20,
                "greater_than_5_years": 15,
                "greater_than_2_years":  10,
                "less_than_2_years": 2
              }
        }

    def test_assessment_evaluator_1(self):
        source = SourceModel(
            qualification="degree",
            work_experience="greater_than_2_years"
        )
        evaluator = AssessmentEvaluator(source=source, rules=self.rules())
        evaluator.evaluate()
        self.assertEqual(35, evaluator.calculate_score())

    def test_assessment_evaluator_2(self):
        source = SourceModel(
            qualification="diploma",
            work_experience="greater_than_2_years"
        )
        evaluator = AssessmentEvaluator(source=source, rules=self.rules())
        evaluator.evaluate()
        self.assertEqual(30, evaluator.calculate_score())

    @patch('app.models.Application.objects.get')
    def test_run_assessment_calculation_handler(self, application_mock):
        source = SourceModel(
            qualification="degree",
            work_experience="greater_than_2_years"
        )
        application_mock.return_value = self.create_data()
        app = application("NEW")

        run_assessment_calculation.send(app, source=source, rules=self.rules())
        assessment_result = AssessmentResult.objects.all()
        self.assertGreater(len(assessment_result), 0)
