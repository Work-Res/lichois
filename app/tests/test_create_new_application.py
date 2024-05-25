import pytest

from datetime import date

from django.test import tag

from app.classes import CreateNewApplicationService
from app.api import NewApplicationDTO
from app.models import ApplicationStatus, Application, ApplicationVersion
from .data import statuses

pytestmark = pytest.mark.django_db

from ..utils import ApplicationProcesses


@tag('cna')
class TestCreateNewApplication:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.new_app = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value, applicant_identifier='317918515',
            status='new', dob="06101990", work_place="01")

        self.create_new = CreateNewApplicationService(new_application=self.new_app)
        ApplicationStatus.objects.all().delete()
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

    def test_application_status_count(self):
        assert ApplicationStatus.objects.count() == len(statuses)

    def test_application_status(self):
        app_status = ApplicationStatus.objects.get(code=self.new_app.status)
        assert app_status.code == self.new_app.status

    def test_get_or_create_application_user(self):
        application_user = self.create_new.get_or_create_application_user()
        user_identifier = application_user.id
        assert application_user is not None
        application_user2 = self.create_new.get_or_create_application_user()
        assert user_identifier == application_user2.id

    def test_get_or_create_application_user_when_user_identifier_none(self):
        self.new_app.applicant_identifier = None
        self.create_new.get_or_create_application_user()
        assert len(self.create_new.response.messages) == 1

    def test_create_application_document(self):
        create_new = CreateNewApplicationService(new_application=self.new_app)
        app_document = create_new.create_application_document()
        assert app_document.document_date == date.today()
        assert app_document.signed_date == date.today()

    def test_get_application_status(self):
        create_new = CreateNewApplicationService(new_application=self.new_app)
        status = create_new.get_application_status()
        assert status.code == self.new_app.status
        # assert status.processes == 'WORK_RESIDENT_PERMIT,residentpermit,visa'
        assert status is not None

    def test_generate_document(self):
        create_new = CreateNewApplicationService(new_application=self.new_app)
        document_number = create_new.generate_document()
        assert document_number == "WR010610199000001-1"

    def test_create(self):
        create_new = CreateNewApplicationService(new_application=self.new_app)
        create_new.create()
        document_number = "WR010610199000001-1"
        app = Application.objects.first()
        assert Application.objects.count() == 1
        assert ApplicationVersion.objects.count() == 1
        assert app.application_document.document_number == document_number
