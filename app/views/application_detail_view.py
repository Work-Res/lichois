from rest_framework import generics

from app.models import Application
from app.api.serializers import ApplicationSerializer


class ApplicationDetailView(generics.ListAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        document_number = self.request.query_params.get('document_number')
        if document_number:
            queryset = queryset.filter(document_number=document_number)
        return queryset
