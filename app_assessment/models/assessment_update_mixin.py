from app.classes.mixins.update_application_mixin import UpdateApplicationMixin


class AssessmentUpdateMixin(UpdateApplicationMixin):

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Update the related application's assessment field to "done"
        if hasattr(self, "document_number") and self.document_number:
            self.update_application_field(
                document_number=self.document_number,
                field_key="assessment",
                field_value="done",
            )
