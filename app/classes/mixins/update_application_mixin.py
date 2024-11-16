from django.db import transaction
from rest_framework.exceptions import ValidationError
from app.models import Application


class UpdateApplicationMixin:

    @transaction.atomic
    def update_application_field(self, document_number, field_key, field_value):
        """
        Update the assessment field in the Application model based on the document number.

        :param document_number: The document number to filter the Application.
        :param assessment_field_value: The value to update the assessment field with.
        :raises ValidationError: If no Application is found with the given document number.
        """

        # Ensure the field_key is a valid field of the Application model
        if not hasattr(Application, field_key):
            raise ValidationError(
                detail=f"Invalid field key: {field_key}.",
                code=400,
            )

        # Perform the update
        try:
            # Retrieve the application instance
            application = Application.objects.get(
                application_document__document_number=document_number
            )

            # Update the field value
            setattr(application, field_key, field_value)

            # Save the instance
            application.save()

        except Application.DoesNotExist:
            raise ValidationError(
                detail=f"No application found with document number {document_number}.",
                code=404,
            )
