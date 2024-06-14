from ..models import Application
from rest_framework.response import Response
from rest_framework.views import APIView
from app.api.serializers import ApplicationCountSerializer

class ApplicationCountView(APIView):
    def get(self, request, *args, **kwargs):
        application_type = self.kwargs.get('application_type')  
        application_type_count = Application.objects.filter(type=application_type).count() 
        data = {
            'application_type_count': application_type_count
        }
        return Response(data)
