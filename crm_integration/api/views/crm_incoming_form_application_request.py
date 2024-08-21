import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm_integration.service import RabbitMQService


class CrmIncomingFormApplicationRequest(APIView):

    def post(self, request, *args, **kwargs):

        try:
            logging.INFO(f"Recievied a requested from CRM. {request.data}")
            rabbitmq_service = RabbitMQService(
                queue_name="citizenship_queue",
                exchange_key="citizenship_exchange"
            )
            rabbitmq_service.publish_message(message=request.data)
            return Response({'message': 'Form submitted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
