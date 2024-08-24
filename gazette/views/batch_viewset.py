import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, APIException

from app.api.common.pagination import StandardResultsSetPagination
from gazette.api.serializers.serializers import BatchGazetteSerializer
from gazette.models import Batch
from gazette.service import ApplicationBatchService
from gazette.service.batch_decision_service import BatchDecisionService
from gazette.views.filter import BatchFilter


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchGazetteSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = BatchFilter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            created_by = request.user.id

            self.logger.info(f"Creating a batch with title: {title}, description: {description}, created_by: {created_by}")
            batch = ApplicationBatchService.create_batch(title, description, created_by)
            serializer = self.get_serializer(batch)

            self.logger.info(f"Successfully created batch with ID: {batch.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            self.logger.error(f"Validation error while creating batch: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Unexpected error while creating batch: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def add_application(self, request, pk=None):
        try:
            batch_id = pk
            application_id = request.data.get('application_id')

            self.logger.info(f"Adding application {application_id} to batch {batch_id}")
            ApplicationBatchService.add_application_to_batch(batch_id, application_id)

            self.logger.info(f"Successfully added application {application_id} to batch {batch_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            self.logger.error(f"Batch or application not found: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            self.logger.error(f"Validation error while adding application to batch: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Unexpected error while adding application to batch: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def add_applications(self, request, pk=None):
        try:
            batch_id = pk
            application_ids = request.data.get('application_ids', [])

            self.logger.info(f"Adding applications {application_ids} to batch {batch_id}")
            ApplicationBatchService.add_applications_to_batch(batch_id, application_ids)

            self.logger.info(f"Successfully added applications to batch {batch_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            self.logger.error(f"Batch or applications not found: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            self.logger.error(f"Validation error while adding applications to batch: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Unexpected error while adding applications to batch: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def remove_application(self, request, pk=None):
        try:
            batch_id = pk
            application_id = request.data.get('application_id')

            self.logger.info(f"Removing application {application_id} from batch {batch_id}")
            ApplicationBatchService.remove_application_from_batch(batch_id, application_id)

            self.logger.info(f"Successfully removed application {application_id} from batch {batch_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            self.logger.error(f"Batch or application not found: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            self.logger.error(f"Validation error while removing application from batch: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Unexpected error while removing application from batch: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def submit_batch(self, request, pk=None):
        try:
            batch_id = pk

            self.logger.info(f"Submitting batch {batch_id}")
            ApplicationBatchService.submit_batch(batch_id)

            self.logger.info(f"Successfully submitted batch {batch_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            self.logger.error(f"Batch not found: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            self.logger.error(f"Validation error while submitting batch: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Unexpected error while submitting batch: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_batch_decision(self, request, pk=None):
        try:
            batch_id = pk
            legal_member_id = request.user.id
            decision = request.data.get('decision')
            comments = request.data.get('comments')

            self.logger.info(f"Creating batch decision for batch {batch_id} by legal member {legal_member_id}")
            BatchDecisionService.create_batch_decision(batch_id, legal_member_id, decision, comments)

            self.logger.info(f"Successfully created batch decision for batch {batch_id}")
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            self.logger.error(f"Validation error while creating batch decision: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            self.logger.error(f"Batch or legal member not found: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            self.logger.error(f"Unexpected error while creating batch decision: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
