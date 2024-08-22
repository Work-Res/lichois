from rest_framework import viewsets
from ..models import PIHistory
from api.serializers import PIHistorySerializer

class PIHistoryViewSet(viewsets.ModelViewSet):
    queryset = PIHistory.objects.all()
    serializer_class = PIHistorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Query parameters
        non_citizen_identifier = self.request.query_params.get('non_citizen_identifier')
        name = self.request.query_params.get('name')
        passport_number = self.request.query_params.get('passport_number')
        fingerprint = self.request.query_params.get('fingerprint')

        # Apply filters based on query parameters
        if non_citizen_identifier:
            queryset = queryset.filter(non_citizen_identifier=non_citizen_identifier)
        elif name:
            queryset = queryset.filter(non_citizen_identifier__name__icontains=name)
        elif passport_number:
            queryset = queryset.filter(non_citizen_identifier__passport_number=passport_number)
        elif fingerprint:
            queryset = queryset.filter(non_citizen_identifier__fingerprint_data=fingerprint)

        return queryset
