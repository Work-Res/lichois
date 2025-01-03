import logging

from app.api.common.web import APIMessage, APIResponse
from app.models import Application
from app.utils import ApplicationStatusEnum, VerificationStatusEnum
from app_assessment.models import Assessment
from app_attachments.models import ApplicationAttachmentVerification

# TODO: Unit testing required


class WorkResidentPermitVerificationValidator:

    def __init__(self, document_number=None):
        self.logger = logging.getLogger(__name__)
        self.document_number = document_number
        self.response = APIResponse()
        try:
            self.application = Application.objects.get(
                application_document__document_number=document_number,
                application_status__code__iexact=ApplicationStatusEnum.VERIFICATION.value,
            )
        except Application.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Incorrect Application Status",
                    details="An application cannot be verified when status is not verification. ",
                ).to_dict()
            )

    def check_if_assessment_exists(self):
        try:
            return Assessment.objects.get(document_number=self.document_number)
        except Assessment.DoesNotExist:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Assessment does not exists.",
                    details="Assessment record must exists first. ",
                ).to_dict()
            )

    def validate(self):
        self.attachments_verifications()

    def is_valid(self):
        """
        Returns True or False after running the validate method.
        """
        # self.check_if_assessment_exists()
        self.validate()
        return True if len(self.response.messages) == 0 else False

    def attachments_verifications(self):
        application_attachments_not_verified = (
            ApplicationAttachmentVerification.objects.filter(
                document_number=self.document_number,
                verification_status__iexact=VerificationStatusEnum.PENDING.value,
            )
        )
        for not_verified in application_attachments_not_verified:
            self.response.messages.append(
                APIMessage(
                    code=400,
                    message="Documents not verified",
                    details=f"Attachment is not verified: {not_verified.document.document_type.name}",
                ).to_dict()
            )
