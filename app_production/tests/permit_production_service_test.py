from django.test import TestCase, tag
from unittest.mock import patch, MagicMock
from datetime import date
from app_personal_details.models import Permit
from workresidentpermit.api.dto.permit_request_dto import PermitRequestDTO
from ..services.permit_production_service import (
    PermitProductionService,
)


@tag("test_permit_production_service")
class PermitProductionServiceTest(TestCase):
    def setUp(self):
        self.request = PermitRequestDTO(
            application_type="type1",
            document_number="123456",
            permit_type="typeA",
            permit_no="",
            date_issued=None,
            place_issue="City",
        )
        self.service = PermitProductionService(self.request)

    @patch("app_checklist.models.SystemParameter.objects.get")
    def test_systems_parameter(self, mock_get):
        mock_get.return_value = MagicMock(application_type="type1")
        result = self.service.systems_parameter()
        self.assertIsNotNone(result)
        mock_get.assert_called_once_with(application_type__icontains="type1")

    @patch("app_checklist.classes.SystemParameterService.calculate_next_date")
    @patch("app_checklist.models.SystemParameter.objects.get")
    def test_calculated_date_duration(self, mock_get, mock_calculate_next_date):
        mock_get.return_value = MagicMock(application_type="type1")
        mock_calculate_next_date.return_value = date(2023, 12, 31)
        result = self.service.calculated_date_duration()
        self.assertEqual(result, date(2023, 12, 31))
        mock_calculate_next_date.assert_called_once()

    @patch("app_personal_details.models.Permit.objects.get")
    def test_get_existing_permit(self, mock_get):
        mock_get.return_value = MagicMock(document_number="123456")
        result = self.service._get_existing_permit()
        self.assertIsNotNone(result)
        mock_get.assert_called_once_with(document_number="123456")

    def test_generate_security_number(self):
        result = self.service.generate_security_number()
        self.assertTrue(result.isdigit())
        self.assertTrue(320000000 <= int(result) <= 3399999999)

    @patch("app_personal_details.models.Permit.objects.create")
    @patch("app_personal_details.models.Permit.objects.get")
    @patch("app_checklist.classes.SystemParameterService.calculate_next_date")
    @patch("app_checklist.models.SystemParameter.objects.get")
    def test_create_new_permit(
        self, mock_get, mock_calculate_next_date, mock_permit_get, mock_permit_create
    ):
        mock_permit_get.side_effect = Permit.DoesNotExist
        mock_get.return_value = MagicMock(application_type="type1")
        mock_calculate_next_date.return_value = date(2023, 12, 31)

        self.service.create_new_permit()

        mock_permit_create.assert_called_once_with(
            document_number="123456",
            permit_type="typeA",
            permit_no=self.service.request.permit_no,
            date_issued=date.today(),
            date_expiry=date(2023, 12, 31),
            place_issue="City",
            security_number=self.service.request.permit_no,
        )
        self.assertEqual(self.service.response.status, "success")
        self.assertTrue(
            any(
                msg["message"] == "Permit created successfully."
                for msg in self.service.response.messages
            )
        )
