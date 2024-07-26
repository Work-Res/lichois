from django.db.models.signals import post_save
from django.dispatch import receiver

from app_information_requests.models import InformationMissingRequest
from app_information_requests.models.information_request_correspondence import InformationRequestCorrespondence
from app_information_requests.service.word import WordDocumentTemplateService


@receiver(post_save, sender=InformationMissingRequest)
def create_missing_info_document(sender, instance, created, **kwargs):
    if created:
        # Trigger the document generation
        service = WordDocumentTemplateService('information_request_template.docx')

        # Define placeholders
        context = {
            'full_name': instance.information_request.submitter.get_full_name(),
            'checklist_request': instance.reason,
            'missing_information_request': instance.description,
            'due_date': instance.information_request.due_date.strftime("%B %d, %Y"),
            'contact_information': 'info@gov.bw',  # Update as needed
            'officer_fullname': 'Jane Smith',  # Update as needed
            'officer_position': 'Application Officer',  # Update as needed
            'officer_contact_information': 'jane.smith@gov.bw'  # Update as needed
        }

        # Generate the document
        output_path = f'/tmp/{instance.id}_missing_info_request.docx'
        service.create_request_letter(context, output_path)

        document = service.replace_placeholders(context)
        service.save_document(document, output_path)

        # Save the generated document to the Attachment model
        with open(output_path, 'rb') as f:
            InformationRequestCorrespondence.objects.create(
                information_request=instance.information_request,
                file=f,
                description="Generated missing information request document"
            )
