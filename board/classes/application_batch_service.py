from ..classes.dto import ApplicationBatchRequestDTO

from ..models import ApplicationBatch
from app.models import Application


class ApplicationBatchService:

    def __init__(self, application_batch_request: ApplicationBatchRequestDTO):
        self.application_batch_request = application_batch_request

    def create_batch(self):
        ApplicationBatch.objects.create(
            applications=Application.objects.filter(id__in=self.application_batch_request.applications),
            batch_type=self.application_batch_request.batch_type
        )
