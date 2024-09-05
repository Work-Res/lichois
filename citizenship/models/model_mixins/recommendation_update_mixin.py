from app.classes.mixins.update_application_mixin import UpdateApplicationMixin
from app.utils.system_enums import ApplicationDecisionEnum
import logging


class RecommendationUpdateMixin(UpdateApplicationMixin):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def save_recommendation(self):
        # Update the related application's assessment field to "done"
        if self.document_number:
            self.update_application_field(
                document_number=self.document_number,
                field_key="recommendation",
                field_value=ApplicationDecisionEnum.DONE.value,
            )
