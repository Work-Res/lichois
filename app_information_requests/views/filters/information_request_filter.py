import django_filters

from app_information_requests.models import InformationRequest


class InformationRequestFilter(django_filters.FilterSet):
    class Meta:
        model = InformationRequest
        fields = {
            'resolution': ['exact'],
            'submitter': ['exact'],
            'process_name': ['icontains'],
            'application_type': ['icontains'],
            'office_location': ['icontains'],
        }
