from unittest.mock import patch

from django.test import TestCase

from app_personal_details.models import Permit

from ..classes import WorkResidentPermitRenewalHistoryService

from app.models import ApplicationRenewalHistory


class TestWorkResidentPermitRenewalHistoryService(TestCase):

    def permit(self):
        permit = Permit()
        permit.permit_no = "3000000001"
        permit.document_number = "WRR00001111"
        permit.permit_type = "WORK_PERMIT_ONLY"
        return permit

    @patch('app_personal_details.models.Permit.objects.get')
    def test_work_create_workresident_permit_renewal(self, mock_permit):
        mock_permit.return_value = self.permit()
        service = WorkResidentPermitRenewalHistoryService(
            document_number="WR000001",
            application_type="WORK_PERMIT_EMERGENCY",
            application_user="XYZ",
            process_name="WORK_RESIDENT_PERMIT"
        )
        service.create_application_renewal_history()
        count = ApplicationRenewalHistory.objects.count()
        self.assertGreater(count, 0)
