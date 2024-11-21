from datetime import date
from django.db import transaction
from model_bakery.recipe import Recipe
from model_mommy import mommy
from django.core.management import call_command

from app.api.dto.application_verification_request_dto import (
    ApplicationVerificationRequestDTO,
)
from app.models.application import Application
from app.classes.application_service import ApplicationService
from app.api.dto.new_application_dto import NewApplicationDTO
from app.api.dto.security_clearance_request_dto import SecurityClearanceRequestDTO
from app.api.serializers.application_verification_request_serializer import (
    ApplicationVerificationRequestSerializer,
)
from app.api.serializers.security_clearance_request_serializer import (
    SecurityClearanceRequestDTOSerializer,
)
from app.models.application_decision_type import ApplicationDecisionType
from app.service.security_clearance_service import SecurityClearanceService
from app.service.verification_service import VerificationService
from app.utils.system_enums import (
    ApplicationDecisionEnum,
    ApplicationProcesses,
    ApplicationStatusEnum,
)
from app.validators.officer_verification_validator import OfficerVerificationValidator
from app.validators.security_clearance_validator import SecurityClearanceValidator
from app_assessment.api.dto.assessment_case_decision_dto import (
    AssessmentCaseDecisionDTO,
)
from app_assessment.api.serializers.assessement_request_serializer import (
    AssessmentRequestSerializer,
)
from app_assessment.service.assessment_case_decision_service import (
    AssessmentCaseDecisionService,
)
from app_assessment.validators.assessment_case_decision_validator import (
    AssessmentCaseDecisionValidator,
)
from app_checklist.models.system_parameter_permit_renewal_period import (
    SystemParameterPermitRenewalPeriod,
)
from app_personal_details.models import Permit, Spouse
from authentication.models import User
from board.choices import VOTE_STATUS
from board.models import (
    BoardDecision,
    BoardMeeting,
    BoardMeetingVote,
    BoardMember,
    MeetingAttendee,
    VotingProcess,
)
from lichois.management.base_command import CustomBaseCommand
from ...models import ResidencePermit, WorkPermit

from ...utils.work_resident_permit_application_type_enum import (
    WorkResidentPermitApplicationTypeEnum,
)


class Command(CustomBaseCommand):
    process_name = ApplicationProcesses.EXEMPTION_CERTIFICATE.value

    def handle(self, *args, **options):
        with transaction.atomic():
            call_command("populate_exemption")
            call_command("populate_exemption_attachments")

            for app in Application.objects.filter(
                process_name=ApplicationProcesses.WORK_RESIDENT_PERMIT.value,
                application_status__code__iexact=ApplicationStatusEnum.VERIFICATION.value,
            ):
                document_number = app.application_document.document_number

                self.perform_verification(document_number)

                self.perform_vetting(document_number)

                self.perform_assessment(document_number)

                board_meeting, board = self.create_board_meeting()

                self.voting_process(board, board_meeting, document_number)

                self.perform_board_decision(document_number, board_meeting)

                permit = Permit.objects.get(document_number=document_number)

                permit.date_issued = date.today()
                permit.date_expiry = date.today()
                permit.save()


    def perform_verification(self, document_number):
        data = {
            "status": "ACCEPTED",
        }
        serializer = ApplicationVerificationRequestSerializer(data=data)
        serializer.is_valid()
        validator = OfficerVerificationValidator(document_number=document_number)
        if validator.is_valid():
            verification_request = ApplicationVerificationRequestDTO(
                document_number=document_number,
                user=None,
                **serializer.validated_data,
            )
            service = VerificationService(verification_request=verification_request)
            return service.create_verification()

    def perform_vetting(self, document_number):
        data = {"status": "ACCEPTED"}
        serializer = SecurityClearanceRequestDTOSerializer(data=data)
        if serializer.is_valid():
            security_clearance_request = SecurityClearanceRequestDTO(
                document_number=document_number,
                user=None,
                **serializer.validated_data,
            )
            validator = SecurityClearanceValidator(
                document_number=document_number,
                status=security_clearance_request.status,
            )
            if validator.is_valid():
                service = SecurityClearanceService(
                    security_clearance_request=security_clearance_request
                )
                return service.create_clearance()

    def perform_board_decision(self, document_number, board_meeting):

        board_decision = BoardDecision.objects.create(
            document_number=document_number,
            decision_outcome="ACCEPTED",
            board_meeting=board_meeting,
            vetting_outcome="ACCEPTED",
        )

        return board_decision

    def perform_assessment(self, document_number):
        data = {"status": "ACCEPTED"}
        serializer = AssessmentRequestSerializer(data=data)
        serializer.is_valid()
        assessment_case_decision = AssessmentCaseDecisionDTO(
            document_number=document_number, decision="ACCEPTED", status="ACCEPTED"
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
        for value in [
            ApplicationDecisionEnum.ACCEPTED.value,
            ApplicationDecisionEnum.APPROVED.value,
            ApplicationDecisionEnum.PENDING.value,
            ApplicationDecisionEnum.REJECTED.value,
        ]:
            ApplicationDecisionType.objects.get_or_create(
                code=value,
                name=value,
                process_types=ApplicationProcesses.EXEMPTION_CERTIFICATE.value,
                valid_from=date(2024, 1, 1),
                valid_to=date(2025, 1, 1),
            )

    def create_board_meeting(self):
        board = mommy.make_recipe("board.board")

        board_meeting = Recipe(
            BoardMeeting,
            title="Sample Board Meeting",
            meeting_date="2024-10-25",
            meeting_start_time="09:00:00",
            meeting_end_time="11:00:00",
            description="This is a sample board meeting description.",
            status="PENDING",
            board=board,
            minutes="Minutes of the board meeting.",
            meeting_type="REGULAR",
            location="Headquarters",
        ).make()
        return board_meeting, board

    def voting_process(self, board, board_meeting, document_number):
        # Create users and board members
        user_data = [
            {
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
            },
            {
                "username": "testuser2",
                "first_name": "Test2",
                "last_name": "User2",
                "email": "testuser2@example.com",
            },
            {
                "username": "testuser3",
                "first_name": "Test3",
                "last_name": "User3",
                "email": "testuser3@example.com",
            },
        ]

        board_members = []
        for user_info in user_data:
            try:
                user = User.objects.get(username=user_info["username"])
            except User.DoesNotExist:
                user = self.create_user(**user_info)
            else:
                board_member = self.create_board_member(board, user)
                board_members.append(board_member)

        meeting_attendees = []
        for board_member in board_members:
            attendee = self.create_meeting_attendee(board_meeting, board_member)
            meeting_attendees.append(attendee)

        voting_process = Recipe(
            VotingProcess,
            board=board,
            status="STARTED",
            document_number=document_number,
            board_meeting=board_meeting,
        ).make()
        # Create board meeting votes
        for attendee in meeting_attendees:
            self.create_board_meeting_vote(attendee, document_number)
            self.stdout.write(self.style.SUCCESS("Successfully voted"))

        voting = VotingProcess.objects.get(document_number=document_number)
        voting.status = "ENDED"
        voting.save()
        return voting_process

    def create_meeting_attendee(self, board_meeting, board_member, status="Present"):
        return MeetingAttendee.objects.create(
            meeting=board_meeting,
            board_member=board_member,
            attendance_status=status,
        )

    def create_user(self, username, first_name, last_name, email):
        return Recipe(
            User,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            is_staff=False,
        ).make()

    def create_board_member(self, board, user):
        return Recipe(
            BoardMember, board=board, user=user, board_join_date="2024-10-25"
        ).make()

    def create_board_meeting_vote(self, meeting_attendee, document_number):
        voting = Recipe(
            BoardMeetingVote,
            meeting_attendee=meeting_attendee,
            document_number=document_number,
            status="APPROVED",
            comments="This is a sample comment",
        ).make()

        return voting

