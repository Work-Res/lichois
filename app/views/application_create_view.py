import json

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api import NewApplication
from app.classes import CreateNewApplication
from app.api.serializers import NewApplicationSerializer


class ApplicationCreateView(APIView):

    """
    Receives a request to create a new application. ( VISA or WORK PERMIT  e.t.c)
    """
    def post(self, request, format=None):
        try:
            serializer = NewApplicationSerializer(data=request.data)
            if serializer.is_valid():
                new_app = NewApplication(
                    process_name=serializer.data.get('process_name'),
                    applicant_identifier=serializer.data.get('applicant_identifier'),
                    status=serializer.data.get('status'),
                    dob=serializer.data.get('dob'),
                    work_place=serializer.data.get('work_place')
                )
                create_new = CreateNewApplication(new_application=new_app)
                create_new.create()
                return JsonResponse(create_new.response.result())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
