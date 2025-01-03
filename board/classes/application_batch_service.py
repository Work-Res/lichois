from ..classes.dto import ApplicationBatchRequestDTO

from django.db import transaction
from app.api.common.web import APIMessage, APIResponse

from ..serializers.application_batch_serializer import ApplicationBatchSerializer

from ..models import ApplicationBatch
from app.models import Application


class ApplicationBatchService:

    def __init__(self, application_batch_request: ApplicationBatchRequestDTO):
        self.application_batch_request = application_batch_request
        self.response = APIResponse()

    @transaction.atomic()
    def create_batch(self):
        batch = ApplicationBatch.objects.create(
            batch_type=self.application_batch_request.batch_type
        )
        for application in Application.objects.filter(
            id__in=self.application_batch_request.applications
        ):
            batch.applications.add(application)
            application.batched = True
            application.save()
        batch.save()
        api_message = APIMessage(
            code=200,
            message="Application batch created successfully.",
            details="An application batch created successfully.",
        )
        self.response.status = "success"
        self.response.data = ApplicationBatchSerializer(batch).data
        self.response.messages.append(api_message.to_dict())
