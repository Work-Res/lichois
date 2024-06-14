import json

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api import NewApplicationDTO
from app.classes import ApplicationService
from app.api.serializers import NewApplicationSerializer


class ApplicationCreateView(APIView):

    """
    Receives a request to create a new application. ( VISA or WORK PERMIT  e.t.c).
        {
           "process_name": "work",
           "applicant_identifier": "",
           "dob": ""
           "work_place": "",
           "full_name": ""
        }
    """
    def post(self, request, format=None):
        try:
            serializer = NewApplicationSerializer(data=request.data)
            if serializer.is_valid():
                new_app = NewApplicationDTO(
                    process_name=serializer.data.get('process_name'),
                    applicant_identifier=serializer.data.get('applicant_identifier'),
                    status=serializer.data.get('status'),
                    dob=serializer.data.get('dob'),
                    work_place=serializer.data.get('work_place'),
                    full_name=serializer.data.get('full_name')
                )
                create_new = ApplicationService(new_application=new_app)
                create_new.create_application()
                return JsonResponse(create_new.response.result())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
