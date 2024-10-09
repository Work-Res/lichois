from django.db import transaction
from rest_framework.exceptions import ValidationError
from app.models import Application
from citizenship.models import Section10bApplicationDecisions


class UpdateSection10bMixin:

    @transaction.atomic
    def update_field(self, document_number, field_key, field_value):
        """
        Update the assessment field in the Application model based on the document number.

        :param document_number: The document number to filter the Application.
        :param assessment_field_value: The value to update the assessment field with.
        :raises ValidationError: If no Application is found with the given document number.
        """

        # Ensure the field_key is a valid field of the Application model
        if not hasattr(Section10bApplicationDecisions, field_key):
            raise ValidationError(
                detail=f"Invalid field key: {field_key}.",
                code=400,
            )

        # Perform the update
        try:
            # Retrieve the application instance
            section10b = Section10bApplicationDecisions.objects.get(
                application__application_document__document_number=document_number
            )

            # Update the field value
            setattr(section10b, field_key, field_value)

            # Save the instance
            section10b.save()

            self.logger.info(
                f"Successfully updated application {document_number} field {field_key} to {field_value}."
            )

            self.logger.info(f"updated section 10b {section10b}")

        except Application.DoesNotExist:
            self.logger.error(
                f"No Section10b found with document number {document_number}."
            )
            raise ValidationError(
                detail=f"No Section10b found with document number {document_number}.",
                code=404,
            )
