from django.test import TestCase

from ..validators import WorkResidentPermitValidator


class TestWorkResidentPermitValidator(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_find_missing_mandatory_fields(self):
       validator = WorkResidentPermitValidator(
           process=None,
           work_resident_permit=None,
           document_number=None)
