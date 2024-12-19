from datetime import date

from faker import Faker

from django.apps import apps

from app.api.dto import ApplicationVerificationRequestDTO, SecurityClearanceRequestDTO
from app.api.serializers import ApplicationVerificationRequestSerializer, SecurityClearanceRequestDTOSerializer
from app.service import VerificationService, SecurityClearanceService
from app.validators import OfficerVerificationValidator, SecurityClearanceValidator
from app_assessment.api.dto import AssessmentCaseDecisionDTO
from app_assessment.api.serializers import AssessmentRequestSerializer
from app_assessment.service.assessment_case_decision_service import AssessmentCaseDecisionService
from app_assessment.validators import AssessmentCaseDecisionValidator
from app_checklist.apps import AppChecklistConfig

from app.models import ApplicationStatus, ApplicationDecisionType
from app.classes import ApplicationService

from app.api import NewApplicationDTO
from app.utils import ApplicationProcesses

from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress, Country
from app_contact.models import ApplicationContact

from app_checklist.models import ClassifierItem
from app_attachments.models import ApplicationAttachment, AttachmentDocumentType
from app.utils import ApplicationStatusEnum
from authentication.models import User
from board.models import BoardDecision, VotingProcess, BoardMeetingVote, MeetingAttendee, BoardMember
from model_bakery.recipe import Recipe
from board.models import BoardMeeting

from django.db.models.signals import post_save


from workresidentpermit.models import WorkPermit

from app.utils import statuses, ApplicationDecisionEnum
from django.test import TestCase
from model_mommy import mommy


class BaseTestSetup(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_config = apps.get_app_config("app_checklist")
        if isinstance(app_config, AppChecklistConfig):
            app_config.ready()

    def application_decision_type(self):
        for value in [
            ApplicationDecisionEnum.ACCEPTED.value,
            ApplicationDecisionEnum.APPROVED.value,
            ApplicationDecisionEnum.PENDING.value,
            ApplicationDecisionEnum.REJECTED.value,
        ]:
            process_types = None
            for process in ApplicationProcesses:
                if process_types:
                    process_types = f"{process_types},{process.value}"
                else:
                    process_types = f"{process.value}"

            ApplicationDecisionType.objects.create(
                code=value,
                name=value,
                process_types=process_types,
                valid_from=date(2024, 1, 1),
                valid_to=date(2025, 1, 1),
            )

    def create_new_application(self):
        self.new_application_dto = NewApplicationDTO(
            process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            applicant_identifier='317918515',
            status=ApplicationStatusEnum.VERIFICATION.value,
            dob="06101990",
            work_place="01",
            application_type=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
            full_name="Test test",
            applicant_type="student"
        )

        self.application_service = ApplicationService(new_application_dto=self.new_application_dto)
        return self.application_service.create_application()

    def create_application_statuses(self):
        for status in statuses:
            ApplicationStatus.objects.create(**status)

    def create_personal_details(self, application, faker):
        return Person.objects.get_or_create(
            document_number=application.application_document.document_number,
            application_version=None,
            first_name=faker.unique.first_name(),
            last_name=faker.unique.last_name(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(
                elements=("single", "married", "divorced")
            ),
            # country_birth=faker.country(),
            # place_birth=faker.city(),
            gender=faker.random_element(elements=("male", "female")),
            occupation=faker.job(),
            qualification=faker.random_element(
                elements=("diploma", "degree", "masters", "phd")
            ),
        )

    def create_address(self, app, faker):
        country = Country.objects.create(name=faker.country())
        return ApplicationAddress.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            po_box=faker.address(),
            apartment_number=faker.building_number(),
            plot_number=faker.building_number(),
            address_type=faker.random_element(
                elements=("residential", "postal", "business", "private", "other")
            ),
            country=country,
            status=faker.random_element(elements=("active", "inactive")),
            city=faker.city(),
            street_address=faker.street_name(),
            private_bag=faker.building_number(),
        )

    def voting_process(self):
        voting_process_recipe = Recipe(
            VotingProcess,
            board=self.board,
            status="ENDED",
            document_number=self.document_number,
            board_meeting=self.board_meeting,
        )
        voting_process_instance = voting_process_recipe.make()
        voting_process_instance.save()
        return voting_process_instance

    def perform_verification(self):
        data = {"status": "ACCEPTED"}
        serializer = ApplicationVerificationRequestSerializer(data=data)
        serializer.is_valid()
        validator = OfficerVerificationValidator(document_number=self.document_number)
        if validator.is_valid():
            verification_request = ApplicationVerificationRequestDTO(
                document_number=self.document_number,
                user=None,
                **serializer.validated_data,
            )
            service = VerificationService(verification_request=verification_request)
            return service.create_verification()

    def perform_vetting(self):
        data = {"status": "ACCEPTED"}
        serializer = SecurityClearanceRequestDTOSerializer(data=data)
        if serializer.is_valid():
            security_clearance_request = SecurityClearanceRequestDTO(
                document_number=self.document_number,
                user=None,
                **serializer.validated_data,
            )
            validator = SecurityClearanceValidator(
                document_number=self.document_number,
                status=security_clearance_request.status,
            )
            if validator.is_valid():
                service = SecurityClearanceService(
                    security_clearance_request=security_clearance_request
                )
                return service.create_clearance()

    def perform_board_decision(self):
        self._board_decision = BoardDecision.objects.create(
            document_number=self.document_number,
            decision_outcome="ACCEPTED",
            board_meeting=self.board_meeting,
            vetting_outcome="ACCEPTED",
        )

    def perform_assessment(self):
        data = {"status": "ACCEPTED"}
        serializer = AssessmentRequestSerializer(data=data)
        serializer.is_valid()
        assessment_case_decision = AssessmentCaseDecisionDTO(
            document_number=self.document_number, decision="ACCEPTED", status="ACCEPTED"
        )
        validator = AssessmentCaseDecisionValidator(
            assessment_case_decision=assessment_case_decision,
        )

        if validator.is_valid():
            service = AssessmentCaseDecisionService(
                assessment_case_decision_dto=assessment_case_decision
            )
            return service.create_assessment()

    def application_decision_type(self):
        for value in [ApplicationDecisionEnum.ACCEPTED.value,
                      ApplicationDecisionEnum.APPROVED.value,
                      ApplicationDecisionEnum.PENDING.value,
                      ApplicationDecisionEnum.REJECTED.value]:
            ApplicationDecisionType.objects.create(
                code=value,
                name=value,
                process_types=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
                valid_from=date(2024, 1, 1),
                valid_to=date(2025, 1, 1)
            )

    def create_user(self, username, first_name, last_name, email):
        return Recipe(
            User,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            is_staff=False
        ).make()

    def create_board_member(self, board, user):
        return Recipe(
            BoardMember,
            board=board,
            user=user,
            board_join_date="2024-10-25"
        ).make()

    def create_meeting_attendee(self, board_meeting, board_member, status="Present"):
        return Recipe(
            MeetingAttendee,
            meeting=board_meeting,
            board_member=board_member,
            attendance_status=status
        ).make()

    def create_board_meeting_vote(self,meeting_attendee, document_number, status="APPROVED"):
        return Recipe(
            BoardMeetingVote,
            meeting_attendee=meeting_attendee,
            document_number=document_number,
            status=status,
            comments="This is a sample comment",
            tie_breaker=None
        ).make()

    def setUp(self) -> None:

        self.create_application_statuses()
        application_version = self.create_new_application()
        app = application_version.application
        self.application = application_version.application
        self.document_number = app.application_document.document_number

        # Create board
        self.board = mommy.make_recipe('board.board')

        # Create board meeting
        self.board_meeting = Recipe(
            BoardMeeting,
            title="Sample Board Meeting",
            meeting_date="2024-10-25",
            meeting_start_time="09:00:00",
            meeting_end_time="11:00:00",
            description="This is a sample board meeting description.",
            status="PENDING",
            board=self.board,
            minutes="Minutes of the board meeting.",
            meeting_type="REGULAR",
            location="Headquarters"
        ).make()

        # Create users and board members
        user_data = [
            {"username": "testuser", "first_name": "Test", "last_name": "User", "email": "testuser@example.com"},
            {"username": "testuser2", "first_name": "Test2", "last_name": "User2", "email": "testuser2@example.com"},
            {"username": "testuser3", "first_name": "Test3", "last_name": "User3", "email": "testuser3@example.com"}
        ]

        board_members = []
        for user_info in user_data:
            user = self.create_user(**user_info)
            board_member = self.create_board_member(self.board, user)
            board_members.append(board_member)

        # Create meeting attendees
        meeting_attendees = [
            self.create_meeting_attendee(self.board_meeting, board_member)
            for board_member in board_members
        ]

        # Create board meeting votes
        for attendee in meeting_attendees:
            self.create_board_meeting_vote(attendee, self.document_number)

        faker = Faker()

        Person.objects.get_or_create(
            document_number=app.application_document.document_number,
            application_version=None,
            first_name=faker.unique.first_name(),
            last_name=faker.unique.last_name(),
            dob=faker.date_of_birth(minimum_age=18, maximum_age=65),
            middle_name=faker.first_name(),
            marital_status=faker.random_element(elements=('single', 'married', 'divorced')),
            country_birth=faker.country(),
            place_birth=faker.city(),
            gender=faker.random_element(elements=('male', 'female')),
            occupation=faker.job(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd'))
        )

        country = Country.objects.create(name=faker.country())
        ApplicationAddress.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            po_box=faker.address(),
            apartment_number=faker.building_number(),
            plot_number=faker.building_number(),
            address_type=faker.random_element(elements=('residential', 'postal', 'business', 'private',
                                                        'other')),
            country=country,
            status=faker.random_element(elements=('active', 'inactive')),
            city=faker.city(),
            street_address=faker.street_name(),
            private_bag=faker.building_number(),
        )

        ApplicationContact.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            contact_type=faker.random_element(elements=('cell', 'email', 'fax', 'landline')),
            contact_value=faker.phone_number(),
            preferred_method_comm=faker.boolean(chance_of_getting_true=50),
            # status=faker.random_element(elements=('active', 'inactive')),
            # description=faker.text(),
        )

        Passport.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            passport_number=faker.passport_number(),
            date_issued=faker.date_this_century(),
            expiry_date=faker.date_this_century(),
            place_issued=faker.city(),
            nationality=faker.country(),
            photo=faker.image_url(),
        )

        classifer_attachment_types = ClassifierItem.objects.filter(
            code__in=['PASSPORT_COPY', 'PASSPORT_PHOTO', 'COVER_LETTER']
        )

        for classifier in classifer_attachment_types:
            attachment_type = AttachmentDocumentType.objects.create(
                code=classifier.code,
                name=classifier.name,
                valid_from=date.today(),
                valid_to=date(2025, 1, 1)
            )
            ApplicationAttachment.objects.create(
                document_number=app.application_document.document_number,
                document_type=attachment_type,
                filename=f"{classifier.name}.pdf",
                storage_object_key="cxxcc",
                description="NNNN",
                document_url="",
                received_date=date.today()
            )

        WorkPermit.objects.create(
            application_version=None,
            document_number=app.application_document.document_number,
            permit_status=faker.random_element(elements=('new', 'renewal')),
            job_offer=faker.text(),
            qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
            business_name=faker.company(),
            type_of_service=faker.text(),
            job_title=faker.job(),
            job_description=faker.text(),
            renumeration=faker.random_int(min=10000, max=100000),
            period_permit_sought=faker.random_int(min=1, max=10),
            has_vacancy_advertised=faker.random_element(elements=('Yes', 'No')),
            reason_no_vacancy_advertised=faker.text(),
            have_funished=faker.boolean(chance_of_getting_true=50),
            reasons_funished=faker.text(),
            time_fully_trained=faker.random_int(min=1, max=10),
            reasons_renewal_takeover=faker.text(),
            reasons_recruitment=faker.text(),
            labour_enquires=faker.text(),
            no_bots_citizens=faker.random_int(min=1, max=10),
            no_non_citizens=faker.random_int(min=1, max=10),
            name=faker.name(),
            educational_qualification=faker.random_element(elements=('diploma', 'degree', 'masters', 'phd')),
            job_experience=faker.text(),
            take_over_trainees=faker.first_name(),
            long_term_trainees=faker.first_name(),
            date_localization=faker.date_this_century(),
            employer=faker.company(),
            occupation=faker.job(),
            duration=faker.random_int(min=1, max=10),
            names_of_trainees=faker.first_name(),
        )

        self.application_decision_type()
