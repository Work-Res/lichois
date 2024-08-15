from app.classes.mixins.update_application_mixin import UpdateApplicationMixin
from app.utils.system_enums import ApplicationDecisionEnum
import logging


class AssessmentUpdateMixin(UpdateApplicationMixin):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def save_assessment(self):
        # Update the related application's assessment field to "done"
        if self.document_number:
            self.update_application_field(
                document_number=self.document_number,
                field_key="assessment",
                field_value=ApplicationDecisionEnum.DONE.value,
            )
