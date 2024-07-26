from email._header_value_parser import ContentType

from django.db import transaction

from app_information_requests.models import InformationRequest, InformationMissingRequest
from app_information_requests.models.information_request_correspondence import InformationRequestCorrespondence
from app_information_requests.service.word import WordDocumentTemplateService
from app_notification.models import Notification
from authentication.models import User


class InformationRequestService:

    def __init__(self, template_path):
        self.document_service = WordDocumentTemplateService(template_path)

    @staticmethod
    @transaction.atomic
    def create_information_request(self,
                                   submitter_id,
                                   process_name,
                                   application_type,
                                   office_location,
                                   due_date, missing_requests_data):
        # Fetch the submitter
        submitter = User.objects.get(id=submitter_id)

        # Create the InformationRequest instance
        info_request = InformationRequest.objects.create(
            resolution=False,
            submitter=submitter,
            process_name=process_name,
            application_type=application_type,
            office_location=office_location,
            due_date=due_date
        )

        # Create InformationMissingRequest instances
        for missing_request_data in missing_requests_data:
            InformationMissingRequest.objects.create(
                parent_object_id=missing_request_data['parent_object_id'],
                parent_type=missing_request_data['parent_type'],
                information_request=info_request,
                reason=missing_request_data['reason'],
                description=missing_request_data['description'],
                is_provided=missing_request_data.get('is_provided', False),
                comment=missing_request_data.get('comment', '')
            )

        # Generate the document and save it as an attachment
        attachment = self.generate_and_save_document(info_request)

        # Create a notification
        self.create_notification(submitter, attachment)

        return info_request

    @staticmethod
    def generate_and_save_document(self, info_request, submitter):
        placeholders = {
            'full_name': info_request.submitter.get_full_name(),
            'checklist_request': ', '.join([req.reason for req in info_request.missing_requests.all()]),
            'missing_information_request': '\n'.join([req.description for req in info_request.missing_requests.all()]),
            'due_date': info_request.due_date.strftime("%B %d, %Y"),
            'contact_information': submitter.email,
            'officer_fullname': submitter.get_full_name(),
            'officer_position': 'NA',
            'officer_contact_information': submitter.email
        }

        output_path = f'/tmp/{info_request.id}_missing_info_request.docx'
        self.document_service.create_request_letter(placeholders, output_path)

        # Save the generated document to the Attachment model
        with open(output_path, 'rb') as f:
            InformationRequestCorrespondence.objects.create(
                information_request=info_request,
                file=f,
                description="Generated missing information request document"
            )

    @staticmethod
    def create_notification(self, user, attachment):
        content_type = ContentType.objects.get_for_model(InformationRequestCorrespondence)
        message = f"A new document has been generated for your information request: {attachment.description}"

        Notification.objects.create(
            user=user,
            content_type=content_type,
            object_id=attachment.id,
            message=message,
            has_attachment=True
        )
