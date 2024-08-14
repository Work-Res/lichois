from app.classes.mixins.update_application_mixin import UpdateApplicationMixin
from app.utils.system_enums import ApplicationDecisionEnum


class AssessmentUpdateMixin(UpdateApplicationMixin):

    def save(self, *args, **kwargs):
        # Update the related application's assessment field to "done"
        if self.document_number:
            self.update_application_field(
                document_number=self.document_number,
                field_key="assessment",
                field_value=ApplicationDecisionEnum.DONE.value,
            )
