from django.db import transaction
from app.api.common.web import APIMessage, APIResponse
from ..api.serializers.prisoner_release_log_serializer import (
    PrisonerReleaseLogSerializer,
)


from ..models import PrisonerReleaseLog, Prisoner


class PrisonerReleaseLogBatchService:

    def __init__(self, prisoner_batch):
        self.prisoner_batch = prisoner_batch
        self.response = APIResponse()

    @transaction.atomic()
    def create_batch(self):
        batch = PrisonerReleaseLog.objects.create()
        for prisoner in Prisoner.objects.filter(
            non_citizen_identifier__in=self.prisoner_batch
        ):
            batch.prisoners.add(prisoner)
            prisoner.batched = True
            prisoner.save()
        batch.save()
        api_message = APIMessage(
            code=200,
            message="Prisoner release log created successfully.",
            details="Prisoner release log created successfully.",
        )
        self.response.status = "success"
        self.response.data = PrisonerReleaseLogSerializer(batch).data
        self.response.messages.append(api_message.to_dict())
