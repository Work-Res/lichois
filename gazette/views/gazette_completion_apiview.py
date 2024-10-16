from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404

from gazette.models import Batch
from gazette.service.gazette_completion_service import GazetteCompletionService
import logging

logger = logging.getLogger(__name__)


class GazetteCompletionAPIView(APIView):
    """
    API View to activate the next task for all applications in the given batch.
    """

    def post(self, request, *args, **kwargs):
        batch_id = request.data.get('batch_id')
        gazette_completion_date = request.data.get('gazette_completion_date')

        # Validate input
        if not batch_id:
            return self._error_response("batch_id is required", status.HTTP_400_BAD_REQUEST)

        gazette_completion_date = self._validate_gazette_date(gazette_completion_date)
        if isinstance(gazette_completion_date, Response):
            return gazette_completion_date  # Return if date validation failed

        # Try activating the next task for the batch
        try:
            batch = get_object_or_404(Batch, id=batch_id)

            if gazette_completion_date:
                self._update_gazette_completion_date(batch, gazette_completion_date)

            self._activate_next_task_for_batch(batch_id)

            return Response({"message": f"Tasks activated for batch {batch_id}"}, status=status.HTTP_200_OK)

        except Exception as e:
            return self._handle_exception(e, batch_id)

    def _validate_gazette_date(self, gazette_completion_date):
        """Validates and parses the gazette completion date."""
        if gazette_completion_date:
            try:
                return datetime.strptime(gazette_completion_date, "%Y-%m-%d").date()
            except ValueError:
                logger.error("Invalid gazette_completion_date format. Expected format: YYYY-MM-DD.")
                return Response(
                    {"error": "Invalid date format for gazette_completion_date. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return None

    def _update_gazette_completion_date(self, batch, gazette_completion_date):
        """Updates the gazette completion date for the batch."""
        batch.gazette_completion_date = gazette_completion_date
        batch.save()
        logger.info(f"Gazette completion date updated to {gazette_completion_date} for batch {batch.id}")

    def _activate_next_task_for_batch(self, batch_id):
        """Activates the next task for all applications in the given batch."""
        gazette_service = GazetteCompletionService(batch_id=batch_id)
        gazette_service.activate_next_task_for_all()
        logger.info(f"Successfully activated next task for all applications in batch {batch_id}")

    def _error_response(self, message, status_code):
        """Helper to return error responses with consistent structure."""
        logger.error(message)
        return Response({"error": message}, status=status_code)

    def _handle_exception(self, exception, batch_id):
        """Handles exceptions and logs the error."""
        logger.error(f"Failed to activate next task for batch {batch_id}. Error: {str(exception)}", exc_info=True)
        return Response({"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
