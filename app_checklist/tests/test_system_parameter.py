# app_checklist/tests/test_system_parameter.py

from django.test import TestCase
from datetime import date, timedelta
from app_checklist.models.system_parameter import SystemParameter
from app_checklist.classes.system_parameters_service import SystemParameterService

class TestSystemParameterService(TestCase):

    def setUp(self):
        # Create test data
        self.system_param_years = SystemParameter.objects.create(
            duration_type='years',
            duration=2,
            application_type='test_app_years',
            valid_from=date(2022, 1, 1),
            valid_to=date(2024, 1, 1)
        )
        self.system_param_months = SystemParameter.objects.create(
            duration_type='months',
            duration=6,
            application_type='test_app_months',
            valid_from=date(2023, 1, 1),
            valid_to=date(2023, 7, 1)
        )
        self.system_param_weeks = SystemParameter.objects.create(
            duration_type='weeks',
            duration=4,
            application_type='test_app_weeks',
            valid_from=date(2023, 5, 1),
            valid_to=date(2023, 5, 29)
        )

    def test_get_by_application_type(self):
        system_param = SystemParameterService.get_by_application_type('test_app_years')
        self.assertEqual(system_param, self.system_param_years)

    def test_calculate_expiry_date_years(self):
        expiry_date = SystemParameterService.calculate_expiry_date(self.system_param_years)
        expected_expiry_date = self.system_param_years.valid_from + timedelta(days=365 * self.system_param_years.duration)
        self.assertEqual(expiry_date, expected_expiry_date)

    def test_calculate_expiry_date_months(self):
        expiry_date = SystemParameterService.calculate_expiry_date(self.system_param_months)
        expected_expiry_date = self.system_param_months.valid_from + timedelta(days=30 * self.system_param_months.duration)
        self.assertEqual(expiry_date, expected_expiry_date)

    def test_calculate_expiry_date_weeks(self):
        expiry_date = SystemParameterService.calculate_expiry_date(self.system_param_weeks)
        expected_expiry_date = self.system_param_weeks.valid_from + timedelta(weeks=self.system_param_weeks.duration)
        self.assertEqual(expiry_date, expected_expiry_date)

    def test_invalid_duration_type(self):
        system_param_invalid = SystemParameter.objects.create(
            duration_type='invalid',
            duration=1,
            application_type='test_app_invalid',
            valid_from=date(2023, 1, 1),
            valid_to=date(2024, 1, 1)
        )
        with self.assertRaises(ValueError):
            SystemParameterService.calculate_expiry_date(system_param_invalid)
