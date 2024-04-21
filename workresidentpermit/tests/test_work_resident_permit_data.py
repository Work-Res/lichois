import pytest

from datetime import date
from app.classes import CreateNewApplication
from app.api import NewApplication
from app.utils import ApplicationProcesses, statuses
from app.models import ApplicationStatus
from ..models import WorkResidencePermit, Spouse, Child, Permit

from ..classes import WorkResidentPermitData


class TestWorkResidentPermitData:


    @pytest.fixture(autouse=True)
    def setup(self):
        self.new_app = NewApplication(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value, applicant_identifier='317918515',
            status='new', dob="06101990", work_place="01")

        self.create_new = CreateNewApplication(new_application=self.new_app)
        ApplicationStatus.objects.all().delete()
        for status in statuses:
            ApplicationStatus.objects.create(
                **status
            )

    def test_search_by_document_number(self):
        create_new = CreateNewApplication(new_application=self.new_app)
        application_version = create_new.create()
        work_permit = WorkResidencePermit.objects.create(
            file_number="NA",
            preferred_method_comm="email",
            preferred_method_comm_value="test@test.com",
            language="en",
            permit_reason="testing testing",
            state_period_required=date.today(),
            propose_work_employment='yes',
            reason_applying_permit='immigrant',
            documentary_proof="work",
            travelled_on_pass="",
            is_spouse_applying_residence="yes",
            ever_prohibited="NA",
            sentenced_before="NA",
            entry_place="NA",
            arrival_date=date.today(),
            application_version=application_version
        )
        Spouse.objects.create(
            spouse_last_name="test",
            spouse_first_name="test",
            spouse_middle_name="NA",
            spouse_maiden_name="NA_NA",
            spouse_country="BW",
            spouse_place_birth="gaborone",
            spouse_dob=date(2000, 1, 1),
            work_resident_permit=work_permit
        )
        Child.objects.create(
            child_first_name="child1",
            child_last_name="child1",
            child_age=18,
            gender="yes",
            work_resident_permit=work_permit,
            is_applying_residence="yes"
        )
        Permit.objects.create(
            permit_type="Type",
            permit_no="",
            date_issued=date.today(),
            date_expiry=date.today(),
            place_issue="gaborone",
            work_resident_permit=work_permit
        )
        permit_data = WorkResidentPermitData(application_version.application.application_document.document_number)
