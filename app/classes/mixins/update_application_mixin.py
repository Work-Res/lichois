# app_assessment/mixins.py

from rest_framework.exceptions import ValidationError
from app.models import Application


class UpdateApplicationMixin:
    def update_application_field(self, document_number, field_key, field_value):
        """
        Update the assessment field in the Application model based on the document number.

        :param document_number: The document number to filter the Application.
        :param assessment_field_value: The value to update the assessment field with.
        :raises ValidationError: If no Application is found with the given document number.
        """
        if field_value and document_number and field_key:
            updated_count = Application.objects.filter(
                application_document__document_number=document_number
            ).update(field_key=field_value)

            if updated_count == 0:
                raise ValidationError(
                    detail=f"No application found with document number {document_number}.",
                    code=404,
                )
