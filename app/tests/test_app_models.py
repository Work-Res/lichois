import pytest

pytestmark = pytest.mark.django_db


class TestApplicationModel:

    def test_str_return(self, application_version_factory):
        application_version = application_version_factory(version_number=1)
        assert application_version.application.application_document.document_number == 'REF/RES/LAB-001'
        assert application_version.application.__str__() == 'Application REF/RES/LAB-001'
        assert application_version.application.application_document.__str__() == 'Document REF/RES/LAB-001'

    def test_all_aa(self):
        pass
