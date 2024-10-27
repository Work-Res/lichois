from django.test import TestCase
from unittest import mock
from datetime import datetime

from app.validators import ApplicationRenewalValidator
from app_personal_details.models import Permit
from app_checklist.models import SystemParameterPermitRenewalPeriod


class ApplicationRenewalValidatorTest(TestCase):

    def setUp(self):
        self.application_type = 'WORK_PERMIT'
        self.permit = Permit(
            document_number="DOC123",
            date_issued=datetime(2022, 1, 1).date(),
            date_expiry=datetime(2024, 1, 1).date()
        )

    @mock.patch('app_checklist.models.SystemParameterPermitRenewalPeriod.objects.get')
    def test_renewal_allowed(self, mock_system_param_get):
        # Mock the system parameter to allow 25% threshold
        mock_system_param_get.return_value = mock.Mock(percent=0.25)

        # Initialize the validator
        validator = ApplicationRenewalValidator(self.permit, self.application_type)

        # Fast forward time to 75% of the permit duration left
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 10, 1)
            self.assertTrue(validator.is_renewal_allowed())

    @mock.patch('app_checklist.models.SystemParameterPermitRenewalPeriod.objects.get')
    def test_renewal_not_allowed(self, mock_system_param_get):
        # Mock the system parameter to allow 25% threshold
        mock_system_param_get.return_value = mock.Mock(percent=0.25)

        # Initialize the validator
        validator = ApplicationRenewalValidator(self.permit, self.application_type)

        # Fast forward time to more than 25% of the duration left
        with mock.patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2022, 6, 1)
            self.assertFalse(validator.is_renewal_allowed())

    @mock.patch('app_checklist.models.SystemParameterPermitRenewalPeriod.objects.get')
    def test_system_parameter_not_found(self, mock_system_param_get):
        # Simulate SystemParameterPermitRenewalPeriod.DoesNotExist exception
        mock_system_param_get.side_effect = SystemParameterPermitRenewalPeriod.DoesNotExist

        with self.assertRaises(ValueError) as context:
            validator = ApplicationRenewalValidator(self.permit, self.application_type)

        self.assertIn('System parameter not found for application type', str(context.exception))

    @mock.patch('app_checklist.models.SystemParameterPermitRenewalPeriod.objects.get')
    def test_invalid_permit_dates(self, mock_system_param_get):
        # Mock the system parameter to allow 25% threshold
        mock_system_param_get.return_value = mock.Mock(percent=0.25)

        invalid_permit = Permit(
            document_number="DOC124",
            date_issued=datetime(2022, 1, 1).date(),
            date_expiry=None
        )

        with self.assertRaises(ValueError) as context:
            validator = ApplicationRenewalValidator(invalid_permit, self.application_type)
            validator.is_renewal_allowed()

        self.assertIn('Invalid permit dates', str(context.exception))
